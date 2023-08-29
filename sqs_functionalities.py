import boto3

sqs = boto3.client('sqs')

'''
queue_name = 'MyQueue'
queue_url = create_sqs_queue(queue_name)
message_body = 'This is a test message.'
'''
def create_sqs_queue(queue_name):
    response = sqs.create_queue(QueueName=queue_name)
    return response['QueueUrl']

def send_message_to_queue(queue_url, message_body):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response

def receive_messages_from_queue(queue_url, max_messages=1):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages
    )
    return response.get('Messages', [])

def delete_message_from_queue(queue_url, receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

