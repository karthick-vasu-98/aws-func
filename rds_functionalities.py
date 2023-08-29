import boto3

# Create an RDS client
rds = boto3.client('rds')

'''
instance_id = 'my-rds-instance'
engine = 'mysql'
instance_class = 'db.t2.micro'
username = 'admin'
password = 'yourpassword'
allocated_storage = 20
db_name = 'mydb'
snapshot_id = 'my-snapshot'
instance_class = 'db.t2.micro'
availability_zone = 'us-east-1a'
subnet_group_name = 'my-subnet-group'
security_group_ids = ['sg-1234567890abcdef0', 'sg-abcdef1234567890']
parameter_group_name = 'my-parameter-group'
parameter_group_family = 'mysql8.0'
parameter_group_description = 'My custom parameter group'
parameters_to_modify = [
    {'ParameterName': 'max_connections', 'ParameterValue': '1000'},
    {'ParameterName': 'innodb_buffer_pool_size', 'ParameterValue': '512MB'}
]
'''
# Create an RDS instance
def create_rds_instance(instance_identifier, db_engine, db_instance_class,
                        master_username, master_password, allocated_storage,
                        db_name, publicly_accessible=False):
    response = rds.create_db_instance(
        DBInstanceIdentifier=instance_identifier,
        Engine=db_engine,
        DBInstanceClass=db_instance_class,
        MasterUsername=master_username,
        MasterUserPassword=master_password,
        AllocatedStorage=allocated_storage,
        DBName=db_name,
        PubliclyAccessible=publicly_accessible
    )
    return response

# Describe an RDS instance
def describe_rds_instance(instance_identifier):
    response = rds.describe_db_instances(DBInstanceIdentifier=instance_identifier)
    return response['DBInstances'][0]

# Modify an RDS instance
def modify_rds_instance(instance_identifier, new_instance_class):
    response = rds.modify_db_instance(
        DBInstanceIdentifier=instance_identifier,
        DBInstanceClass=new_instance_class
    )
    return response

# Delete an RDS instance
def delete_rds_instance(instance_identifier, skip_final_snapshot=True):
    response = rds.delete_db_instance(
        DBInstanceIdentifier=instance_identifier,
        SkipFinalSnapshot=skip_final_snapshot
    )
    return response

# Create a manual DB snapshot (backup)
def create_db_snapshot(instance_identifier, snapshot_identifier):
    response = rds.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_identifier,
        DBInstanceIdentifier=instance_identifier
    )
    return response

# Restore a DB instance from a snapshot
def restore_db_instance(instance_identifier, snapshot_identifier, db_instance_class,
                        availability_zone, db_subnet_group_name, publicly_accessible=False):
    response = rds.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier=instance_identifier,
        DBSnapshotIdentifier=snapshot_identifier,
        DBInstanceClass=db_instance_class,
        AvailabilityZone=availability_zone,
        DBSubnetGroupName=db_subnet_group_name,
        PubliclyAccessible=publicly_accessible
    )
    return response

# Modify security groups for an RDS instance
def modify_security_groups(instance_identifier, security_group_ids):
    response = rds.modify_db_instance(
        DBInstanceIdentifier=instance_identifier,
        VpcSecurityGroupIds=security_group_ids
    )
    return response

# Create a custom parameter group
def create_parameter_group(parameter_group_name, family, description):
    response = rds.create_db_parameter_group(
        DBParameterGroupName=parameter_group_name,
        DBParameterGroupFamily=family,
        Description=description
    )
    return response

# Modify parameters in a parameter group
def modify_parameters(parameter_group_name, parameters):
    response = rds.modify_db_parameter_group(
        DBParameterGroupName=parameter_group_name,
        Parameters=parameters
    )
    return response

# Apply a parameter group to an RDS instance
def apply_parameter_group(instance_identifier, parameter_group_name):
    response = rds.modify_db_instance(
        DBInstanceIdentifier=instance_identifier,
        DBParameterGroupName=parameter_group_name
    )
    return response

