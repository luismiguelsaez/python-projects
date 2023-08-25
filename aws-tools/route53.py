import boto3
import re

def get_zone_by_name(name_pattern: str, private: bool)->list[dict]:
    session = boto3.Session()
    route53_client = session.client('route53')

    # Match the zone name by regex
    zones = [ z for z in route53_client.list_hosted_zones_by_name()['HostedZones'] if re.match(name_pattern, z['Name']) and z['Config']['PrivateZone'] == private ]
    return zones

def get_zone_records(zone_id: str, name_pattern: str = '.*')->list[dict]:
    session = boto3.Session()
    route53_client = session.client('route53')

    # Get the zone records
    records = [ r for r in route53_client.list_resource_record_sets(HostedZoneId=zone_id)['ResourceRecordSets'] if re.match(name_pattern, r['Name']) ]
    return records