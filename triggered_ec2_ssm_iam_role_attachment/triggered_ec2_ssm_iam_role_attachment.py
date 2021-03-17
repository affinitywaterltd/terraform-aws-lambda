import boto3
import os

ROLE_NAME = os.environ['role_name']

ec2client = boto3.client('ec2')

stsclient = boto3.client('sts')
account_id = stsclient.get_caller_identity()['Account']

iam_role_arn = "arn:aws:iam::{}:instance-profile/{}".format(account_id, ROLE_NAME)


def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instanceid = event['detail']['instance-id']
    #instanceid = 'i-0496caa71efa41cbe' #In case manual adding is needed for testing
    instance = ec2.Instance(id=instanceid)
    iam_role = instance.iam_instance_profile
    
    print (iam_role)
    if iam_role == None:
      print ('Updating IAM Role to: {}'.format(iam_role_arn))
      # Set instance IAM Role
      ec2client.associate_iam_instance_profile(
         IamInstanceProfile={
            'Arn': iam_role_arn,
            'Name': ROLE_NAME
         },
         InstanceId=instanceid
      )   
      print ('IAM Role Updated')

#End Function