import boto3

# Initialize a Boto3 EMR client
emr_client = boto3.client('emr')

# Configuration for the EMR cluster
emr_cluster_config = {
    'Name': 'MyEMRCluster',
    'LogUri': 's3://your-bucket/logs/',  # Replace with your S3 bucket for logs
    'ReleaseLabel': 'emr-6.3.0',  # Replace with the desired EMR release label
    'Applications': [{'Name': 'Spark'}],  # You can add more applications if needed
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'Master nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',  # Replace with the desired instance type
                'InstanceCount': 1,
            },
            {
                'Name': 'Core nodes',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': 'm5.xlarge',  # Replace with the desired instance type
                'InstanceCount': 2,
            }
        ],
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False,
    },
    'VisibleToAllUsers': True,  # Set to True if you want the cluster to be visible to all users
    'JobFlowRole': 'EMR_EC2_DefaultRole',  # Replace with your EMR role
    'ServiceRole': 'EMR_DefaultRole'  # Replace with your EMR service role
}

# Create an EMR cluster
def create_emr_cluster(cluster_config):
    try:
        response = emr_client.run_job_flow(**cluster_config)
        return response['JobFlowId']
    except Exception as e:
        print("Error creating EMR cluster:", e)
        return None

def delete_emr_cluster(cluster_id):
    try:
        response = emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print("Error deleting EMR cluster:", e)
        return False

def get_emr_cluster_status(cluster_id):
    try:
        response = emr_client.describe_cluster(ClusterId=cluster_id)
        return response['Cluster']['Status']['State']
    except Exception as e:
        print("Error getting EMR cluster status:", e)
        return None

def start_emr_cluster(cluster_id):
    try:
        response = emr_client.start_job_flow(JobFlowIds=[cluster_id])
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print("Error starting EMR cluster:", e)
        return False

def stop_emr_cluster(cluster_id):
    try:
        response = emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print("Error stopping EMR cluster:", e)
        return False


'''
cluster_id_to_submit_job = 'j-XXXXXXXXXXXX'  # Replace with your cluster ID
step_name = 'MyEMRStep'
action_on_failure = 'CONTINUE'  # Set to 'TERMINATE_CLUSTER' if you want to terminate the cluster on step failure
jar_path = 's3://your-bucket/your-job.jar'  # Replace with the path to your job JAR file
main_class = 'com.example.MyJobMainClass'  # Replace with the main class of your job
args = ['arg1', 'arg2']  # Replace with the arguments for your job
'''
def submit_emr_job(cluster_id, step_name, action_on_failure, jar_path, main_class, args):
    try:
        step = {
            'Name': step_name,
            'ActionOnFailure': action_on_failure,
            'HadoopJarStep': {
                'Jar': jar_path,
                'MainClass': main_class,
                'Args': args
            }
        }
        response = emr_client.add_job_flow_steps(JobFlowId=cluster_id, Steps=[step])
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print("Error submitting EMR job:", e)
        return False