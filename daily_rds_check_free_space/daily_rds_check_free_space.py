import json
import boto3
import math
from datetime import datetime, timedelta

def do_rounding (input_value):
    """Rounds the input value up to the nearest number divisible by 5 and returns the result
       i.e. 22 is rounded to 25"""
    BASE=5
    if input_value % BASE == 0:
        return(input_value)
    else:
        return int(math.floor(input_value/BASE) * BASE + BASE)

def lambda_handler(event, context):
    # Create RDS client
    rds = boto3.client('rds')
    # Create Cloudwatch client
    cw = boto3.client('cloudwatch', region_name='eu-west-1')
    # Create an SNS client
    sns = boto3.client('sns', region_name='eu-west-1')
    # Create an STS client
    sts = boto3.client('sts', region_name='eu-west-1')

    # Get AccountId
    ACCOUNT_ID = sts.get_caller_identity()["Account"]

    CLOUDWATCH_PERIOD=10800
    TOPIC_ARN_WARNING="arn:aws:sns:eu-west-1:" + ACCOUNT_ID + ":sns_alerts_dba_warning"
    TOPIC_ARN_INFO="arn:aws:sns:eu-west-1:" + ACCOUNT_ID + ":sns_alerts_dba_info"
    EMAIL_BODY=""
    WARNING=0

    try:
        # Get details of all RDS instances
        dbs = rds.describe_db_instances()
        for db in dbs['DBInstances']:
            DBINFO = [db['DBInstanceIdentifier'],db['DBInstanceStatus'],db['AllocatedStorage']]

            # If RDS instance is available get cloudwatch metric for FreeStorageSpace,
            # if it is not available the cloudwatch metric will not be available
            if DBINFO[1] == 'available':
                response = cw.get_metric_statistics(
                    Namespace='AWS/RDS',
                    MetricName='FreeStorageSpace',
                    Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': DBINFO[0]}],
                    StartTime=datetime.utcnow() - timedelta(seconds=CLOUDWATCH_PERIOD),
                    EndTime=datetime.utcnow(),
                    Period=CLOUDWATCH_PERIOD,
                    Statistics=['Average', 'Minimum', 'Maximum']
                 )
            else:
                EMAIL_BODY += DBINFO[0] + ' is ' + DBINFO[1] + ' skipping free space check\n'
                continue

            dp = response['Datapoints']

            if len(dp) == 0:
                print ('WARN: Response from CloudWatch was empty for ',DBINFO[0])

            for d in response['Datapoints']:
                freegb=round(d['Minimum']/1024/1024/1024,1)
                DBINFO.append(freegb)

            FREEPCT = round(DBINFO[3] / DBINFO[2] * 100,1)
            USED = DBINFO[2] - DBINFO[3]

            # If Allocated storage is:
            #   > 100Gb then low is considered < 10% will recommend new size to give ~20% free
            #   > 50Gb and < 100Gb then low is considered < 20% will recommend new size to give ~30% free
            #   < 50Gb then low is considered < 30% will recommend new size to give ~40% free

            if DBINFO[2] > 100:
                if FREEPCT < 10:
                    TARGETUSEDPCT=80
                    NEWSIZE = do_rounding(USED / TARGETUSEDPCT * 100)
                    EMAIL_BODY += '---->  Warning ' + DBINFO[0] + ' has ' + str(DBINFO[2]) + 'Gb allocated of which ' + str(DBINFO[3]) + 'Gb is free, that is only ' + str(FREEPCT) + '% free. Suggest increasing to ' + str(NEWSIZE) + 'Gb\n'
                    WARNING = WARNING + 1
                else:
                    EMAIL_BODY += DBINFO[0] + ' has ' + str(DBINFO[2]) + 'Gb allocated of which ' + str(DBINFO[3]) + 'Gb is free, that is ' + str(FREEPCT) + '% free\n'
            elif DBINFO[2] > 50 and DBINFO[2] <= 100:
                if FREEPCT < 20:
                    TARGETUSEDPCT=70
                    NEWSIZE = do_rounding(USED / TARGETUSEDPCT * 100)
                    EMAIL_BODY += '---->  Warning ' + DBINFO[0] + ' has ' + str(DBINFO[2]) + 'Gb allocated of which ' + str(DBINFO[3]) + 'Gb is free, that is only ' + str(FREEPCT) + '% free. Suggest increasing to ' + str(NEWSIZE) + 'Gb\n'
                    WARNING = WARNING + 1
                else:
                    EMAIL_BODY += DBINFO[0] + ' has ' + str(DBINFO[2]) + 'Gb allocated of which ' + str(DBINFO[3]) + 'Gb is free, that is ' + str(FREEPCT) + '% free\n'
            else:
                if FREEPCT < 30:
                    TARGETUSEDPCT=60
                    NEWSIZE = do_rounding(USED / TARGETUSEDPCT * 100)
                    EMAIL_BODY += '---->  Warning ' + DBINFO[0] + ' has ' + str(DBINFO[2]) + 'Gb allocated of which ' + str(DBINFO[3]) + 'Gb is free, that is only ' + str(FREEPCT) + '% free. Suggest increasing to ' + str(NEWSIZE) + 'Gb\n'
                    WARNING = WARNING + 1
                else:
                    EMAIL_BODY += DBINFO[0] + ' has ' + str(DBINFO[2]) + 'Gb allocated of which ' + str(DBINFO[3]) + 'Gb is free, that is ' + str(FREEPCT) + '% free\n'

    except Exception as error:
        print (error)

    print (EMAIL_BODY)

    if WARNING > 0:
        TOPIC_ARN = TOPIC_ARN_WARNING
    else:
        TOPIC_ARN = TOPIC_ARN_INFO

    # Publish a message.
    sns.publish(Message=EMAIL_BODY, TopicArn=TOPIC_ARN)
