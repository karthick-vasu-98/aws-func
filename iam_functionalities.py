import boto3

# Create an IAM client
iam = boto3.client('iam')

# Create a user
def create_user(username):
    response = iam.create_user(UserName=username)
    return response['User']

# Create a group
def create_group(groupname):
    response = iam.create_group(GroupName=groupname)
    return response['Group']

# Create an IAM role
def create_role(rolename, trust_policy):
    response = iam.create_role(
        RoleName=rolename,
        AssumeRolePolicyDocument=trust_policy
    )
    return response['Role']

# Attach a policy to a user or group
def attach_policy_to_user(username, policy_arn):
    iam.attach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

def attach_policy_to_group(groupname, policy_arn):
    iam.attach_group_policy(
        GroupName=groupname,
        PolicyArn=policy_arn
    )

def attach_policy_to_role(rolename, policy_arn):
    iam.attach_role_policy(
        RoleName=rolename,
        PolicyArn=policy_arn
    )

# Detach a policy from a user, group, or role
def detach_policy_from_user(username, policy_arn):
    iam.detach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

def detach_policy_from_group(groupname, policy_arn):
    iam.detach_group_policy(
        GroupName=groupname,
        PolicyArn=policy_arn
    )

def detach_policy_from_role(rolename, policy_arn):
    iam.detach_role_policy(
        RoleName=rolename,
        PolicyArn=policy_arn
    )

# List all policies
def list_policies():
    response = iam.list_policies()
    return response['Policies']

# List all users
def list_users():
    response = iam.list_users()
    return response['Users']

# List all groups
def list_groups():
    response = iam.list_groups()
    return response['Groups']

# List all roles
def list_roles():
    response = iam.list_roles()
    return response['Roles']

# List attached policies for a user, group, or role
def list_attached_policies(username=None, groupname=None, rolename=None):
    if username:
        response = iam.list_attached_user_policies(UserName=username)
    elif groupname:
        response = iam.list_attached_group_policies(GroupName=groupname)
    elif rolename:
        response = iam.list_attached_role_policies(RoleName=rolename)
    return response['AttachedPolicies']

'''
role_arn = 'arn:aws:iam::123456789012:role/MyRole'  # Replace with your role ARN
session_name = 'my-session'
'''
def generate_temporary_credentials(role_arn, session_name, duration_seconds=3600):
    """
    Generate temporary security credentials using an IAM role.

    :param role_arn: The ARN of the IAM role to assume.
    :param session_name: A name for the assumed role session.
    :param duration_seconds: The duration for which the credentials will be valid.
    :return: Temporary credentials dictionary.
    """
    sts_client = boto3.client('sts')

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=duration_seconds
    )

    credentials = response['Credentials']
    return {
        'AccessKeyId': credentials['AccessKeyId'],
        'SecretAccessKey': credentials['SecretAccessKey'],
        'SessionToken': credentials['SessionToken'],
        'Expiration': credentials['Expiration']
    }


'''new_user = create_user('exampleuser')
new_group = create_group('examplegroup')
new_role = create_role('examplerole', trust_policy={...})  # Replace with your trust policy

policy_arn = 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'  # Example policy

attach_policy_to_user(new_user['UserName'], policy_arn)
attach_policy_to_group(new_group['GroupName'], policy_arn)
attach_policy_to_role(new_role['RoleName'], policy_arn)

# Example list users, groups, roles, and attached policies
print("Users:", list_users())
print("Groups:", list_groups())
print("Roles:", list_roles())

print("Attached policies for user:", list_attached_policies(username=new_user['UserName']))
print("Attached policies for group:", list_attached_policies(groupname=new_group['GroupName']))
print("Attached policies for role:", list_attached_policies(rolename=new_role['RoleName']))'''
