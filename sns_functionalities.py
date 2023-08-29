import boto3

sns = boto3.client('sns')

'''
topic_name = 'MyTopic'
topic_arn = create_sns_topic(topic_name)
protocol = 'email'  # Replace with your desired protocol (e.g., 'email', 'sms', 'lambda')
endpoint = 'your-email@example.com'  # Replace with your endpoint (e.g., email address, phone number)
message = 'This is a test message.'
subject = 'Test Subject'
'''
def create_sns_topic(topic_name):
    response = sns.create_topic(Name=topic_name)
    return response['TopicArn']

def subscribe_to_topic(topic_arn, protocol, endpoint):
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol=protocol,
        Endpoint=endpoint
    )
    return response['SubscriptionArn']

def publish_to_topic(topic_arn, message, subject=None):
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )
    return response

def list_sns_topics():
    response = sns.list_topics()
    return response['Topics']


