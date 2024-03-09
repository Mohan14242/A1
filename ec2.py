import boto3

# Specify your AWS credentials and region
aws_access_key_id = 'AKIAXTIDON6QYMMZKN5Z'
aws_secret_access_key = 'HvJOFwSd9eiy4oEIqIEulyiZ9tLJoxpC9F2DwrLl'
region_name = 'us-east-1'

# Create an EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Get all running EC2 instances
response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Extract instance details (name and public)
instances = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_name = [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']
        instance_details = {
            'Name': instance_name[0] if instance_name else 'N/A',
            'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
        }
        instances.append(instance_details)

# Print and append to file
output_file_path = 'inventory.ini'

with open(output_file_path, 'w') as output_file:
    for instance in instances:
        output_file.write(f"[{instance['Name']}] \n {instance['Name']} ansible_host={instance['PublicIpAddress']} ansible_user=centos ansible_ssh_pass=DevOps321 \n")
