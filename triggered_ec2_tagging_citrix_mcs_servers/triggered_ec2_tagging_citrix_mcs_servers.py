import boto3
import os

ENVIRO = os.environ['environment']
ACCOUNT = os.environ['account']



def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instanceid = event['detail']['instance-id']
    #instanceid = 'i-04023499492a99d13' #In case manual adding is needed for testing
    instance = ec2.Instance(id=instanceid)
    
    choices_env = {'prod': "Production", 'uat': "UAT", 'sit': "SIT", 'dev': "Development"}
    environment_tag = choices_env.get(ENVIRO, 'default')
    print (environment_tag)
    
    choices_org = {'afb': "AFB"}
    organisation_tag = choices_org.get(ACCOUNT, 'Affinity Water')
    print (organisation_tag)
    
    mytags = [
    {
       "Key" : "Backup",
       "Value" : "False"
    },
    {
       "Key" : "Organisation",
       "Value" : organisation_tag
    },
    {
       "Key" : "BusinessOwner",
       "Value" : "Chris Grey"
    },
    {   "Key": "BusinessUnit",
        "Value": "Infrastructure"
    },
    {
       "Key" : "ServiceOwner",
       "Value" :"Travis De Coning"
    },
    {
       "Key" : "ServiceLevel",
       "Value" : "Gold"
    },
    {
       "Key" : "CostCentre",
       "Value" : "P023611"
    },
    {
       "Key" : "Quadrant",
       "Value" : "Q1"
    },
    {
       "Key" : "ApplicationName",
       "Value" : "Citrix"
    },
    {
       "Key" : "ApplicationType",
       "Value" :"Citrix"
    },
    {
       "Key" : "Description",
       "Value" : "Citrix Application Server"
    },
    {
       "Key" : "Environment",
       "Value" : environment_tag
    },
    {
       "Key" : "Maintenance",
       "Value" : "Citrix Mananged"
    },
    {
       "Key" : "CreatedBy",
       "Value" : "Citrix"
    },
    {
        "Key" : "CreationDate",
        "Value" : "CitrixDaily"
    },
    {
       "Key" : "OperatingSystem",
       "Value" : "Windows Server 2016"
    },
    {
       "Key" : "Scheduler:Startstop",
       "Value" : "False"
    },
    {
       "Key" : "Scheduler:Snapshot",
       "Value" : "False"
    }
    ]
    
    for tag in instance.tags:
        if 'XdConfig' in tag['Key']:
            
            instance.create_tags(
                Tags=mytags
            )    
            print ('citrix')

    