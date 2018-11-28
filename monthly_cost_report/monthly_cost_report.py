import boto3
import datetime
import time
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

# Set up resource calls
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')
rds = boto3.client('rds')
iam = boto3.client('iam')

#Email settings

SES_SMTP_USER="AKIAJKTBC7JXJNT7CREQ"
SES_SMTP_PASSWORD="AgjSKqx+l3QwPSeRXauzlYFFcVMTRaobJKb5gaGyQje5"

MAIL_FROM = 'tim.ellis@affinitywater.co.uk'
MAIL_TO = ['tim.ellis@affinitywater.co.uk']
MAIL_SUBJECT="AWS Monthly Report"
MAIL_BODY=MAIL_SUBJECT + '\n'
filepath = '/tmp/monthly.csv'

#Set up email server using AWS SMPTP

def mail(fromadd,to, subject, text, attach):
       msg = MIMEMultipart()
       msg['From'] = fromadd
       msg['To'] = ", ".join(to)
       msg['Subject'] = subject
       msg.attach(MIMEText(text))
       part = MIMEBase('application', 'octet-stream')
       part.set_payload(open(attach, 'rb').read())
       Encoders.encode_base64(part)
       part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
       msg.attach(part)
       mailServer = smtplib.SMTP("email-smtp.eu-west-1.amazonaws.com", 587)
       mailServer.ehlo()
       mailServer.starttls()
       mailServer.ehlo()
       mailServer.login(SES_SMTP_USER, SES_SMTP_PASSWORD)
       mailServer.sendmail(fromadd, to, msg.as_string())
       print "Email sent"
       # Should be mailServer.quit(), but that crashes...
       mailServer.close()
       
def servers():  # Write instance tags to file

    instances = ec2.instances.all()

    #Open local file to write
    f = open(filepath, 'w')
    f.write("Name, Type, Size, Platform, CreationDate, CostCentre, Quadrant, State, Description, Encryption\n")
    
    for i in instances:
        try:
            for tag in i.tags:
                    try:
                        name = (item for item in i.tags if item["Key"] == "Name" ).next()
                    except StopIteration:
                        name['Value'] = 'Unknown'
                        
                    try:
                        createdate = (item for item in i.tags if item["Key"] == "CreationDate" ).next()
                    except StopIteration:
                        createdate['Value'] = 'Unknown'
    
                    try:
                        costcentre  = (item for item in i.tags if item["Key"] == "CostCentre" ).next()
                    except StopIteration:
                        costcentre['Value'] = 'Unknown'
                    
                    try:
                        quadrant = (item for item in i.tags if item["Key"] == "Quadrant" ).next()
                    except StopIteration:
                        quadrant['Value'] = 'Unknown'
                    
                    try:
                        description = (item for item in i.tags if item["Key"] == "Description" ).next()
                    except StopIteration:
                        description['Value'] = 'Unknown'

        except:
            print i.id

        EC2 = 'EC2'

        f.write('%s,%s,%s,%s,%s,%s,%s,%s, %s\n' %(name['Value'], EC2, i.instance_type, i.platform, createdate['Value'], costcentre['Value'], quadrant['Value'], i.state['Name'], description['Value']))
        
def databases(): # Write DB instance tags to file
    
        #Open local file to write
    f = open(filepath, 'a')

    databases = rds.describe_db_instances()
    for db in databases['DBInstances']:
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
                dbcostcentre  = (item for item in taglist if item["Key"] == "CostCentre" ).next()
            except:
                dbcostcentre['Value'] = 'Unknown'
                
        for tag in taglist:
            try:
                dbquadrant  = (item for item in taglist if item["Key"] == "Quadrant" ).next()
            except:
                dbquadrant['Value'] = 'Unknown'
                
        for tag in taglist:
            try:
                dbdescription  = (item for item in taglist if item["Key"] == "Description" ).next()
            except:
                dbdescription['Value'] = 'Unknown'
                
        RDS = 'RDS'

        f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(dbname, RDS, dbsize, dbengine, dbcreatedate, dbcostcentre['Value'], dbquadrant['Value'], dbstatus, dbdescription['Value'], dbencryption))
        
def lambda_handler(event, context):
    
    # Get Account Name

    paginator = iam.get_paginator('list_account_aliases')
    for response in paginator.paginate():
        alias = (response['AccountAliases'][0])
        
    MAIL_SUBJECT = "AWS Monthly Report - " + alias
    
    servers()
    databases()

    # Send emails
    mail(MAIL_FROM, MAIL_TO, MAIL_SUBJECT, MAIL_BODY, filepath)
    print "Email sent"
