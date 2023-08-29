import boto3
import botocore

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

"vpc_id = 'vpc-XXXXXXXXXXXXXXXXX'  # Replace with your VPC ID"
def create_security_group(group_name, description, vpc_id):
    try:
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        return response['GroupId']
    except Exception as e:
        print("Error creating security group:", e)
        return None

def create_key_pair(key_name):
    try:
        response = ec2_client.create_key_pair(KeyName=key_name)
        return response['KeyMaterial']
    except Exception as e:
        print("Error creating key pair:", e)
        return None

'''
new_ebs_volume_id = create_ebs_volume(10, 'us-east-1a')  # Replace with your desired size and availability zone
'''
def create_ebs_volume(size, availability_zone):
    try:
        response = ec2_client.create_volume(
            Size=size,
            AvailabilityZone=availability_zone
        )
        return response['VolumeId']
    except Exception as e:
        print("Error creating EBS volume:", e)
        return None

def list_instances():
    try:
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            instances.extend(reservation['Instances'])
        return instances
    except botocore.exceptions.ClientError as e:
        print("Error listing instances:", e)
        return []

def start_instance(instance_id):
    try:
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        return response
    except botocore.exceptions.ClientError as e:
        print("Error starting instance:", e)
        return None

def stop_instance(instance_id):
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        return response
    except botocore.exceptions.ClientError as e:
        print("Error stopping instance:", e)
        return None

'''
instance_params = {
    'ImageId': 'ami-xxxxxxxxxxxxxxxxx',  # Replace with your desired AMI ID
    'InstanceType': 't2.micro',           # Replace with your desired instance type
    'KeyName': 'your-key-pair-name',      # Replace with your key pair name
    'MinCount': 1,
    'MaxCount': 1
}
'''
def create_new_instance(params):
    try:
        instance = ec2_resource.create_instances(**params)
        return instance[0].id if instance else None
    except Exception as e:
        print("Error creating instance:", e)
        return None

def get_instance_status(instance_id):
    try:
        instance = ec2_resource.Instance(instance_id)
        return instance.state['Name']
    except Exception as e:
        print("Error getting EC2 instance status:", e)
        return None

def reboot_instance(instance_id):
    try:
        response = ec2_client.reboot_instances(InstanceIds=[instance_id])
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print("Error rebooting instance:", e)
        return False