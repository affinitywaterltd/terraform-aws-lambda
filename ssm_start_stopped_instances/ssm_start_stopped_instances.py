import json
import boto3
import time
from random import randrange

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Perform random sleep to ensure that concurrent executions to not exceed the rate limit of the API
    time.sleep(randrange(20))
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
                )
            
            
    return {
        'statusCode': 200,
        'body': json.dumps('Completed')
    }
