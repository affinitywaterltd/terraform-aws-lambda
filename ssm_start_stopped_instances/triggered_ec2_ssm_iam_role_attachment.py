import json
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    
    ssmMaintenanceWindow = event['ssmMaintenanceWindow']
    print("Checking for instances with ssmMaintenanceWindow tag value - {}".format(ssmMaintenanceWindow))
    
    response = ec2.describe_instances(
        Filters = [
            {
                "Name": "instance-state-name",
                "Values": [
                    "stopped"
                ]
            },
            {
                "Name": "tag:ssmMaintenanceWindow",
                "Values": [
                    ssmMaintenanceWindow
                ]
            }
        ]
    )
    
    # Loop through response
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            
            # Actions for each individual InstanceId
            instanceId = instance['InstanceId']
            print("Starting InstanceId - {}".format(instanceId))
            startResponse = ec2.start_instances(
                    InstanceIds = [
                        instanceId
                    ],
                    DryRun = True
                )
            
            
    return {
        'statusCode': 200,
        'body': json.dumps('Completed')
    }
