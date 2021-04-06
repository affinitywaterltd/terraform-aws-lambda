import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import time
import re
import smtplib
import os      #required to fetch environment varibles
import hmac    #required to compute the HMAC key
import hashlib #required to create a SHA256 hash
import base64  #required to encode the computed key
import sys     #required for system functions (exiting, in this case)

AWS_REGION = 'eu-west-1'

# Set up resource calls
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')
rds = boto3.client('rds')
iam = boto3.client('iam')
ses = boto3.client('ses',region_name=AWS_REGION)

#Email settings

SES_SMTP_USER = os.environ['smtp_ses_user']
SES_SMTP_PASSWORD_RAW = os.environ['smtp_ses_password']

SENDER = 'infra@affinitywater.co.uk'
RECIPIENT = 'infra@affinitywater.co.uk'
SUBJECT = "AWS Monthly Report"
BODY = SUBJECT + '\n'
CHARSET = "UTF-8"

filepath = '/tmp/monthly.csv'


#Set up email server using AWS SMPTP

def mail(RECIPIENT, SENDER, SUBJECT, BODY, attach, alias):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)
    
    att = MIMEApplication(open(filepath, 'rb').read())
    att.add_header('Content-Disposition','attachment',filename="{}.csv".format(alias))
    if os.path.exists(filepath):
        print("File exists")
    else:
        print("File does not exists")
       
    msg.attach(msg_body)
    msg.attach(att)
    try:
    #Provide the contents of the email.
        response = ses.send_raw_email(
            Source=msg['From'],
            Destinations=[
                msg['To']
            ],
            RawMessage={
                'Data':msg.as_string(),
            }
        )
    except ClientError as e:
        return(e.response['Error']['Message'])
    else:
        return("Email sent! Message ID:", response['MessageId'])
       
def servers():  # Write instance tags to file

    instances = ec2.instances.all()
    
    #Open local file to write
    f = open(filepath, 'w')
    f.write("Name, Type, Size, Platform, CreationDate, CostCentre, Quadrant, State, Description, Encryption\n")
    
    for i in instances:
        processerr = 'false'
        try:
            for tag in i.tags:
                    try:
                        name = (item for item in i.tags if item["Key"] == "Name" ).__next__()
                    except StopIteration:
                        name['Value'] = 'Unknown'
                        print ("Name Unknown - {}".format(i.id))
                        
                    try:
                        createdate = (item for item in i.tags if item["Key"] == "CreationDate" ).__next__()
                    except StopIteration:
                        createdate['Value'] = 'Unknown'
                        print ("CreationDate Unknown - {}".format(i.id))
    
                    try:
                        costcentre  = (item for item in i.tags if item["Key"] == "CostCentre" ).__next__()
                    except StopIteration:
                        costcentre['Value'] = 'Unknown'
                        print ("CostCentre Unknown - {}".format(i.id))
                    
                    try:
                        quadrant = (item for item in i.tags if item["Key"] == "Quadrant" ).__next__()
                    except StopIteration:
                        quadrant['Value'] = 'Unknown'
                        print ("Quadrant Unknown - {}".format(i.id))
                    
                    try:
                        description = (item for item in i.tags if item["Key"] == "Description" ).__next__()
                    except StopIteration:
                        description['Value'] = 'Unknown'
                        print ("Description Unknown - {}".format(i.id))
        except:
            print ("exception - {}".format(i.id))
            processerr = 'true'

        EC2 = 'EC2'
        if processerr == 'false':
            f.write('%s,%s,%s,%s,%s,%s,%s,%s, %s\n' %(name['Value'], EC2, i.instance_type, i.platform, createdate['Value'], costcentre['Value'], quadrant['Value'], i.state['Name'], description['Value']))
        else:
            print (i)
        
def databases(): # Write DB instance tags to file
    
        #Open local file to write
    f = open(filepath, 'a')

    databases = rds.describe_db_instances()
    for db in databases['DBInstances']:
        processdberr = 'false'
        try:
            dbname = db['DBInstanceIdentifier']
            dbsize = db['DBInstanceClass']
            dbengine = db['Engine']
            dbstatus = db['DBInstanceStatus']
            dbcreatedate = db['InstanceCreateTime'].strftime("%Y-%m-%d")
            dbencryption = db['StorageEncrypted']
    
            
            currentdb = db['DBInstanceArn']
            taglist = rds.list_tags_for_resource(ResourceName = currentdb)['TagList']
            
            for tag in taglist:
                try:
                    dbcostcentre  = (item for item in taglist if item["Key"] == "CostCentre" ).__next__()
                except:
                    dbcostcentre['Value'] = 'Unknown'
                    
            for tag in taglist:
                try:
                    dbquadrant  = (item for item in taglist if item["Key"] == "Quadrant" ).__next__()
                except:
                    dbquadrant['Value'] = 'Unknown'
                    
            for tag in taglist:
                try:
                    dbdescription  = (item for item in taglist if item["Key"] == "Description" ).__next__()
                except:
                    dbdescription['Value'] = 'Unknown'
        except:
            print ("exception - {}".format(dbname))
            processdberr = 'true'
        if processdberr == 'false':            
            RDS = 'RDS'
            f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(dbname, RDS, dbsize, dbengine, dbcreatedate, dbcostcentre['Value'], dbquadrant['Value'], dbstatus, dbdescription['Value'], dbencryption))
        else:
            print (dbname)
            
def lambda_handler(event, context):
    
    # Get Account Name

    paginator = iam.get_paginator('list_account_aliases')
    for response in paginator.paginate():
        alias = (response['AccountAliases'][0])
        
    SUBJECT = "AWS Monthly Report - " + alias
    
    servers()
    databases()

    # Send emails
    mail(RECIPIENT, SENDER, SUBJECT, BODY, filepath, alias)
    print ("Email sent")
