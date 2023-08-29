import boto3
import botocore

ec2_client = boto3.client('ec2')

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
        ec2_resource = boto3.resource('ec2')
        instance = ec2_resource.create_instances(**params)
        return instance[0].id if instance else None
    except Exception as e:
        print("Error creating instance:", e)
        return None
