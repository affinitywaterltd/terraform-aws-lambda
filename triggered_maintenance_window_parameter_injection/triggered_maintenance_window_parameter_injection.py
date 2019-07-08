import json
import boto3
import os      #required to fetch environment varibles

TASK_NAME_FILTER = os.environ['task_name_filter']

ssmclient = boto3.client('ssm')

def lambda_handler(event, context):
    eventdetail = event['detail']
    eventmwid = eventdetail['window-id']
    eventmwtaskid = eventdetail['window-task-id']
    
    print ("Event Window: " + str(eventmwid))
    print ("Event Task: " + str(eventmwtaskid))

    # Retrieve Maintenance Window
    mwindows = ssmclient.get_maintenance_window(WindowId=eventmwid)
    mwname = mwindows['Name']
    
    # Retrieve Maintenance Window Tasks
    mwtask = ssmclient.get_maintenance_window_task(WindowId=eventmwid, WindowTaskId=eventmwtaskid)
    mwtaskname = mwtask['Name']
    mwtaskid = mwtask['WindowTaskId']
    print ("Task Name: " + str(mwtaskname))   
    
    # Check if task name matches searched for task name
    if TASK_NAME_FILTER in mwtaskname:
        # Expand task paramters
        try:
            taskparamters = mwtask['TaskInvocationParameters']
            taskparamters1 = taskparamters['Automation']
            taskparamters2 = taskparamters1['Parameters']
            taskparamters3 = taskparamters2['TagValue']
    
            parametervalue = taskparamters3[0]
            print("Currently Set: " + parametervalue)
        except:
            print("Cannot retrieve parameters")
            parametervalue = ""
        #Check if parameters already set - without this, the cloudwatch event will trigger everytime and cause a continuous loop
        if mwname in parametervalue:
            # Parameter already set - do nothing
            print("No Update required")
        else:
            # Update Maintenance Task
            ssmclient.update_maintenance_window_task(WindowId=eventmwid, WindowTaskId=eventmwtaskid,TaskInvocationParameters={"Automation":{"DocumentVersion":"$LATEST","Parameters":{"TagValue":[mwname]}}} )
            #ssmclient.update_maintenance_window_task(WindowId=eventmwid, WindowTaskId=eventmwtaskid,TaskInvocationParameters={"Automation":{"DocumentVersion":"$LATEST"}} )
            print ("Task Updated: " + str(mwtaskname))
    return 'Completed'
