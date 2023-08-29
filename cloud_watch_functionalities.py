import boto3
import datetime

cloudwatch = boto3.client('cloudwatch')

'''
metric_name = 'CPUUtilization'  # Replace with the metric you want to retrieve
namespace = 'AWS/EC2'  # Replace with the namespace of the service
dimension_name = 'InstanceId'  # Replace with the dimension you want to filter by
dimension_value = 'i-0123456789abcdef0'  # Replace with the specific value of the dimension
start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
end_time = datetime.datetime.utcnow()
period = 300  # 5-minute period
statistic = 'Average'  # Choose the statistic you want to analyze ('Average', 'Sum', 'Min', 'Max', etc.)
comparison_operator = 'GreaterThanOrEqualToThreshold'
threshold = 80.0  # Set your desired threshold value
evaluation_periods = 3
period = 300  # 5-minute period
statistic = 'Average'  # Choose the statistic you want to use ('Average', 'Sum', 'Min', 'Max', etc.)
alarm_actions = ['arn:aws:sns:us-east-1:123456789012:MyTopic']  # Replace with your SNS topic ARN
alarm_description = 'Alarm for high CPU utilization'
'''
def get_metric_data(metric_name, namespace, dimension_name, dimension_value,
                    start_time, end_time, period=300, statistic='Average'):
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': dimension_name,
                                'Value': dimension_value
                            },
                        ]
                    },
                    'Period': period,
                    'Stat': statistic,
                    'Unit': 'Count'
                },
                'ReturnData': True
            },
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    if 'MetricDataResults' in response:
        for result in response['MetricDataResults']:
            print("Timestamp:", result['Timestamp'])
            print("Value:", result['Values'][0])
            print()

def create_cloudwatch_alarm(alarm_name, metric_name, namespace, comparison_operator,
                            threshold, evaluation_periods, period, statistic, alarm_actions,
                            alarm_description, dimensions=None):
    dimensions = dimensions or []
    
    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        ComparisonOperator=comparison_operator,
        EvaluationPeriods=evaluation_periods,
        MetricName=metric_name,
        Namespace=namespace,
        Period=period,
        Statistic=statistic,
        Threshold=threshold,
        AlarmDescription=alarm_description,
        AlarmActions=alarm_actions,
        Dimensions=dimensions
    )
    return response
