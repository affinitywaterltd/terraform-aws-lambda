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

   instance = ec2.Instance(id=instanceid)
   iam_role = instance.iam_instance_profile
   print ('{} - Current IAM Role - {}'.format(instanceid, iam_role))
   if iam_role == None:
      print ('{} - Updating IAM Role to - {}'.format(instanceid, iam_role_arn))
      # Set instance IAM Role
      ec2client.associate_iam_instance_profile(
         IamInstanceProfile={
            'Arn': iam_role_arn,
            'Name': ROLE_NAME
         },
         InstanceId=instanceid
      )   
      print ('{} - Successfully Updated IAM Role to - {}'.format(instanceid, iam_role_arn))
      return 0
   else:
      print ('{} - IAM Role already assigned - {}'.format(instanceid, iam_role))
      return 0
#End Function