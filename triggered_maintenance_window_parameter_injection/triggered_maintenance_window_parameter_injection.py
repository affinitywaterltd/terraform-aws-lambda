import json
import boto3
import os      #required to fetch environment varibles

TASK_TYPE = os.environ['task_type']
TASK_NAME_FILTER = os.environ['task_name_filter']

ssmclient = boto3.client('ssm')
ec2client = boto3.client('ec2')

def lambda_handler(event, context):
    
    print ("Filtering Type: " + str(TASK_TYPE))

    # Retrieve all Maintenance Windows
    mwindows = ssmclient.describe_maintenance_windows()
    
    # Iterate through all MWs
    for mwindow in mwindows['WindowIdentities']:
        mwid = mwindow['WindowId']
        mwname = mwindow['Name']
        print ("Checking Window: " +str(mwid))
        
        # Retrieve Maintenance Window Tasks for MW that match filtered criteria
        mwtasks = ssmclient.describe_maintenance_window_tasks(WindowId=mwid, Filters=[{'Key': 'TaskType', 'Values': [TASK_TYPE]}])
        for mwtask in mwtasks['Tasks']:
            mwtaskname = mwtask['Name']
            mwtaskid = mwtask['WindowTaskId']
            
            # Check if task name matches searched for task name
            if TASK_NAME_FILTER in mwtaskname:
                print ("Task Name: " + str(mwtaskname))
                
                # Update Maintenance Task
                ssmclient.update_maintenance_window_task(WindowId=mwid, WindowTaskId=mwtaskid,TaskInvocationParameters={"Automation":{"Parameters":{"TagValue":[mwname]}}} )
                print ("Task Updated: " + str(mwtaskname))
    return 'Completed'
