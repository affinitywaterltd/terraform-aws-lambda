import boto3
import sys
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
        log_nextToken = "initial"
        while log_nextToken is not None:
            print("Run - " + log_nextToken)
            if log_nextToken == "initial":
                print("Getting Initial Log Groups")
                log_groups = client.describe_log_groups(limit=50)
            else:
                print("Getting Batch Log Groups")
                log_groups = client.describe_log_groups(limit=50, nextToken=log_nextToken)
                print("Successfully Obtained Batch Log Groups")
            try:
                log_nextToken = log_groups['nextToken']
            except:
                log_nextToken = None
                print("Final Batch")
            log_groups = log_groups['logGroups']
            for log_group in log_groups:
                try:
                    log_group_name = log_group['logGroupName']
                    try:
                        log_group_retention = log_group['retentionInDays']
                    except:
                        log_group_retention = 0
                    try:
                        log_group_stored_bytes = log_group['storedBytes']
                    except:
                        log_group_stored_bytes = 0
                    
                    print (log_group_name + " - " + str(log_group_retention) + " - " + str(log_group_stored_bytes))
                    
                    if log_group_stored_bytes == 0:
                        try:
                            print ("Log Group Empty - DELETING - " + log_group_name)
                            client.delete_log_group(logGroupName=log_group_name)
                            print ("Log Group Empty - DELETED - " + log_group_delete_response)
                        except:
                            print ("normal error during deletion")
                            
                    if OVERWRITE == "true":
                        try:
                            response = client.put_retention_policy(logGroupName=log_group_name,retentionInDays=RETENTION_POLICY_DAYS)
                            print ("Retenion policy updated successfully")
                        except:
                            print ("An error occurred whilst updating log group - " + log_group_name) 
                    #end if
                except:
                    print ("Log Group Empty - DELETED - " + log_group_delete_response)
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
        #end while
    except:
        print("Unexpected error:", sys.exc_info()[0])
#end fucntion