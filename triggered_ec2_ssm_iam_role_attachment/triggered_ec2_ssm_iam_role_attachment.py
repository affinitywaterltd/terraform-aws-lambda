import boto3
import os

ENVIRO = os.environ['environment']
ACCOUNT = os.environ['account']


def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instanceid = event['detail']['instance-id']
    #instanceid = 'i-0496caa71efa41cbe' #In case manual adding is needed for testing
    instance = ec2.Instance(id=instanceid)
    iam_role = instance.iam_instance_profile

    if iam_role == null:
      # Set instance IAM Role
      instance.associate_iam_instance_profile(
         IamInstanceProfile={
            'Arn': 'arn:aws:iam::633033879498:instance-profile/ssm_role',
            'Name': 'ssm_role'
         },
         InstanceId=instanceid
      )   
      print ('IAM Role Updated')

#End Function