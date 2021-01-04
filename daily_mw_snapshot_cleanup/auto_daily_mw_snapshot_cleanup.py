from datetime import datetime, timedelta, timezone
import datetime
import boto3

ec2_client = boto3.client('ec2')

class Ec2Instances(object):
    
    def __init__(self, region):
        print("region "+ region)
        self.ec2 = boto3.client('ec2', region_name=region)
    
    def delete_snapshots(self, older_days=14):
        delete_snapshots_num = 0
        imagesList = self.get_images()
        
        for image in imagesList:
            str_creation_date = image['CreationDate']
            #print("CreationDate String: " + str_creation_date)
            
            fmt_creation_date = datetime.datetime.strptime(str_creation_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            print("CreationDate Formatted: " + str(fmt_creation_date))
            
            print("Cutoff time: " + str(self.get_delete_data(older_days))) 
            print("-------------")
            print("-------------")
            
            if (fmt_creation_date < self.get_delete_data(older_days)):
                print("Deregistering image %s" % image['ImageId'])
                amiResponse = ec2_client.deregister_image(
                    ImageId=image['ImageId'],
                )
                #print(amiResponse)
            print("-------------")

            block_device_mappings = image['BlockDeviceMappings']
            #print("block_device_mapping: %s", block_device_mappings)
            #print("mappings: %s", len(block_device_mappings))
            
            for block_device_mapping in block_device_mappings:
                if "Ebs" in block_device_mapping:
                    device = block_device_mapping['Ebs']
                    #print("ebs: %s", device)
                    snapshot_id = device['SnapshotId']
                    print("snapshot_id: %s", snapshot_id)
                    snapResponse = ec2_client.delete_snapshot(
                        SnapshotId=snapshot_id)
                    #print(snapResponse)
                    print("Deleted snapshot: %s ", snapshot_id)
                    delete_snapshots_num = delete_snapshots_num + 1

        return delete_snapshots_num
                
    def get_images(self):
        images = self.ec2.describe_images(Filters=[{'Name': 'name', 'Values': ['MaintenanceWindow*']}])
        #print("filtered images " + str(images))
        return images['Images']

    def get_delete_data(self, older_days):
        delete_time = datetime.datetime.now(tz=None) - timedelta(days=older_days)
        return delete_time;
            
def lambda_handler(event, context):
    print("event " + str(event))
    print("context " + str(context))
    region_name = "eu-west-1"
    instances = Ec2Instances(region_name)
    deleted_counts = instances.delete_snapshots(14)
    print("deleted_counts for region "+ str(region_name) +" is " + str(deleted_counts))
    return 'completed'