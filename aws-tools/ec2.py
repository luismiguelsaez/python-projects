import boto3
import re
from json import loads, dumps

session = boto3.Session()
ec2_client = session.client('ec2')

def get_ami_id(name_pattern: str = "*", max_results: int = 10, owners: list[str] = ["amazon"], archs: list[str] = ["x86_64"])->dict:
    
    amis = ec2_client.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [name_pattern]
            },
            {
                'Name': 'state',
                'Values': ['available']
            },
            {
                'Name': 'architecture',
                'Values': archs
            },
            {
                'Name': 'virtualization-type',
                'Values': ['hvm']
            },
            {
                'Name': 'hypervisor',
                'Values': ['xen']
            },
            {
                'Name': 'root-device-type',
                'Values': ['ebs']
            },
            {
                'Name': 'manifest-location',
                'Values': ['amazon/*']
            }
        ],
        Owners=owners,
        MaxResults=max_results
    )

    return amis['Images']
