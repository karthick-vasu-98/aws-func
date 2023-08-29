import fnmatch
from io import StringIO
import botocore.session

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


        


        
