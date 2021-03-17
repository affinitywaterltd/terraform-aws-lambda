import boto3
import os

ENVIRO = os.environ['environment']
ACCOUNT = os.environ['account']



def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instanceid = event['detail']['instance-id']
    #instanceid = 'i-0496caa71efa41cbe' #In case manual adding is needed for testing
    instance = ec2.Instance(id=instanceid)
    
    for tag in instance.tags:
        if 'XdConfig' in tag['Key']:
            for tag in instance.tags:
                if tag["Key"] == 'Name':
                    #Find instance name to work out environment
                    instance_name = tag['Value']
                    print ('Instance Name: ' + instance_name)
                #End If    
            #End For
        
            # Convert AWS account environment into Evnironemtn tag as backup if cannot be calculated from instance name
            choices_env = {'prod': "Production", 'uat': "UAT", 'sit': "SIT", 'dev': "Development"}
            environment_tag = choices_env.get(ENVIRO, 'default')
            print ('Account Environment Tag: ' + environment_tag)
            
            # Calculate environment from instance name
            instance_name_env = instance_name[3:6]
            choices_instanceenv = {'PRD': "Production", 'UAT': "UAT", 'SIT': "SIT", 'DEV': "Development"}
            instanceenvironment_tag = choices_instanceenv.get(instance_name_env, environment_tag)
            print ('Instance Environment Tag: ' + instanceenvironment_tag)
            
            # Calculate Organisation from AWS account
            choices_org = {'afb': "AfB"}
            organisation_tag = choices_org.get(ACCOUNT, 'AWL')
            print ('Organisation: ' + organisation_tag)
            
            # Configure Tag values
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
               "Value" : instanceenvironment_tag
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
               "Key" : "Terraform",
               "Value" : "False"
            },
            {
               "Key" : "ssmMaintenanceWindow",
               "Value" : "False"
            }
            ]
            
            # Set instance Tags
            instance.create_tags(
                Tags=mytags
            )    
            print ('Tags Updated')
        #End if
    #End For
#End Function