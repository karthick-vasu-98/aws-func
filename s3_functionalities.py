'''
The functions to create, read, delete in AWS s3 using botocore module
'''
import json
import datetime
import boto3
from io import StringIO
import botocore.session
from botocore.exceptions import NoCredentialsError


s3 = boto3.client('s3')

def get_aws_session():
    return botocore.session.get_session()

def get_s3_client():
    return get_aws_session().create_client('s3')

def get_bucket_key_from_uri(uri):
    result = False
    msg = 'Error'
    key = bucket = None
    try:
        if uri.startswith('s3://'):
            uri_obj_list = uri[5:].split('/')
            bucket = uri_obj_list[0]
            key = '/'.join(uri_obj_list[1:])
            result = True
            msg = 'Success'
        else:
            msg = 'Not a valid URI'
        return result, msg, key, bucket
    except Exception as e:
        print('Error :', e)

def read_s3_file(uri):
    result = False
    msg = 'Error'
    file_content = None
    try:
        client = get_s3_client()
        s_result, msg, key, bucket = get_bucket_key_from_uri(uri=uri)
        if s_result and bucket and key:
            obj = client.get_object(Bucket=bucket, Key=key)
            try:
                file_content = obj['Body'].read()
                result = True
                msg = 'Success'
            except Exception as e:
                print('Client Object Error :', e)
            return result, msg, file_content
    except Exception as e:
        print('Error :', e)

def create_empty_file(uri):
    result = False
    msg = 'Error'
    client = get_s3_client()
    s_result, msg, key, bucket = get_bucket_key_from_uri(uri=uri)
    if s_result and bucket and key:
        response = client.put_object(Bucket=bucket, Key=key, Body='')
        if response['ResponseMetadata']['HTTPStatuscode'] == 200:
            result = True
            msg = 'Success'
    return result, msg

def delete_s3_folder_items(uri):
    result = False
    msg = 'Error'
    client = get_s3_client()
    s_result, msg, key, bucket = get_bucket_key_from_uri(uri=uri)
    if s_result and bucket and key:
        folder_items = client.list_objects(Bucket=bucket, Prefix=key)
        if 'Contents' in folder_items.keys():
            delete_item_obj = [{'Key':x['key']} for x in folder_items['Contents']]
            client.delete_objects(Bucket=bucket, Delete={'Objects':delete_item_obj})
            result = True
            msg = 'Success'
    return result, msg

def set_bucket_policy(bucket_name):
    bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
        ]
    }
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
    return

'''
object_key = 'objects-key'
acl = 'private', 'public-read', 'public-read-write', etc.
'''
def set_object_acl(object_key, acl, bucket_name):
    object_key = object_key
    acl = acl
    s3.put_object_acl(Bucket=bucket_name, Key=object_key, ACL=acl)
    return

'''
username = 'your-iam-user'
bucket_arn = f'arn:aws:s3:::{bucket_name}/*'
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": bucket_arn
        }
    ]
}
'''
def set_iam_policies(username, policy_document, bucket_arn):
    iam = boto3.client('iam')
    policy_arn = iam.create_policy(
        PolicyName='S3AccessPolicy',
        PolicyDocument=json.dumps(policy_document)
    )['Policy']['Arn']

    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
    return
        
def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """
    Generate a presigned URL for temporary access to an S3 object.

    :param bucket_name: The name of the S3 bucket.
    :param object_key: The key of the S3 object.
    :param expiration: The expiration time of the URL in seconds (default is 1 hour).
    :return: The presigned URL.
    """
    s3_client = boto3.client('s3')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        return presigned_url
    except NoCredentialsError:
        return None
