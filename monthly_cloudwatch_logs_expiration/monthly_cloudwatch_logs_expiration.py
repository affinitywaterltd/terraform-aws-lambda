import boto3
import os      #required to fetch environment varibles

client = boto3.client('logs')

RETENTION_POLICY_DAYS = 180

def lambda_handler(event, context):
    
    try:
        OVERWRITE = os.environ['overwrite'].lower()
    except:
        OVERWRITE = "false"
    
    print ("Overwrite enabled - " + OVERWRITE)
    
    try:
        log_groups = client.describe_log_groups()
        log_groups = log_groups['logGroups']
        for log_group in log_groups:
            try:
                log_group_name = log_group['logGroupName']
                log_group_retention = log_group['retentionInDays']
                print (log_group_name + " - " + str(log_group_retention))
                if OVERWRITE == "true":
                    try:
                        print ("Overwrite Enabled - updating log group - " + log_group_name)
                        response = client.put_retention_policy(logGroupName=log_group_name,retentionInDays=RETENTION_POLICY_DAYS)
                        print ("Retenion policy updated successfully")
                    except:
                        print ("An error occurred whilst updating log group - " + log_group_name) 
                #end if
            except:
                # Retention Policy not set
                print (log_group_name + " - Not Set")
                print ("Retention Policy will be applied - " + str(RETENTION_POLICY_DAYS) + " days")
                try:
                    response = client.put_retention_policy(logGroupName=log_group_name,retentionInDays=RETENTION_POLICY_DAYS)
                    print ("Retenion policy updated successfully")
                except:
                    print ("An error occurred whilst updating log group - " + log_group_name)
            #end try
        #end for
    except:
        print ("An error occurred")
#end fucntion