import boto3

lambda_client = boto3.client('lambda')
logs_client = boto3.client('logs')

'''
function_name = 'my-lambda-function'
role_arn = 'arn:aws:iam::123456789012:role/my-lambda-role'
handler = 'my_lambda_function.handler'
runtime = 'python3.8'
code_zip = b'...zip file content...'  # Replace with your Lambda code zip
updated_code_zip = b'...new zip file content...'  # Replace with your updated code zip
updated_handler = 'my_lambda_function_v2.handler'
updated_runtime = 'python3.11.5'
invocation_payload = '{"key": "value"}'
'''
def create_lambda_function(function_name, role_arn, handler, runtime, code_zip):
    response = lambda_client.create_function(
        FunctionName=function_name,
        Role=role_arn,
        Handler=handler,
        Runtime=runtime,
        Code={'ZipFile': code_zip}
    )
    return response

def update_lambda_code(function_name, code_zip):
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=code_zip
    )
    return response

def update_lambda_configuration(function_name, role_arn, handler, runtime):
    response = lambda_client.update_function_configuration(
        FunctionName=function_name,
        Role=role_arn,
        Handler=handler,
        Runtime=runtime
    )
    return response

def invoke_lambda_function(function_name, payload):
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
        Payload=payload
    )
    return response['Payload'].read().decode('utf-8')

'''
function_name = 'my-lambda-function'
s3_bucket = 'my-s3-bucket'
s3_prefix = 'my-s3-prefix'

s3_arn = f'arn:aws:s3:::{s3_bucket}'
s3_event_source_arn = f'{s3_arn}/{s3_prefix}'
'''
def setup_lambda_trigger(function_name, source_arn, batch_size=10):
    response = lambda_client.create_event_source_mapping(
        EventSourceArn=source_arn,
        FunctionName=function_name,
        BatchSize=batch_size,
        StartingPosition='LATEST'  # Use 'TRIM_HORIZON' to process older records
    )
    return response

def get_lambda_log_streams(function_name):
    response = logs_client.describe_log_streams(
        logGroupName='/aws/lambda/' + function_name,
        orderBy='LastEventTime',
        descending=True
    )
    return response['logStreams']

def get_logs_for_stream(log_group_name, log_stream_name):
    response = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    return response['events']