import boto3
import re
from json import loads, dumps

session = boto3.Session()
ec2_client = session.client('ec2')

def get_ebs_volumes_by_status(status: str)->list[dict]:
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': [status]
            }
        ]
    )

    return volumes['Volumes']

def delete_ebs_volumes_by_status(status: str, dry_run: bool = True)->list[dict]:
    volumes = get_ebs_volumes_by_status(status)
    deleted_volumes = []
    for volume in volumes:
        deleted_volumes.append(volume)
        print(f"Deleting {volume['VolumeId']}")
        if not dry_run:
            ec2_client.delete_volume(VolumeId=volume['VolumeId'])

    return deleted_volumes

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
