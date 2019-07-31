import boto3

ENVIRO = os.environ['environment']
ACCOUNT = os.environ['account']

switch (ENVIRO) {
   case "prod":  environment_tag = "Production";
                  break;
   case "uat":  environment_tag = "UAT";
                  break;
   case "sit":  environment_tag = "SIT";
                  break;
   case "dev":  environment_tag = "Development";
                  break;
   default: environment_tag = "Unknown";
}

switch (ACCOUNT) {
   case "afb":  organisation_tag = "AFB";
                  break;
   default: organisation_tag = "Affinity Water";
}


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


def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instanceid = event['detail']['instance-id']
    #instanceid = 'i-09fd5c8c23f52b699' #In case manual adding is needed for testing
    instance = ec2.Instance(id=instanceid)
    
    
    for tag in instance.tags:
        if 'XdConfig' in tag['Key']:
            
            instance.create_tags(
            Tags=mytags
            )    
            print 'citrix'

    