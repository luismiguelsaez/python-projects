import ecr, sns, route53, ec2
from json import dumps, loads


if __name__ == "__main__":

  # Get EBS volumes
  #volumes = ec2.delete_ebs_volumes_by_status(status='in-use')
  #for volume in volumes:
  #  print(f"Volume: {volume['VolumeId']} ({volume['Size']}GB) -> {volume['State']}")
  #  if volume['Attachments']:
  #    print(f"  Attached to: {volume['Attachments'][0]['InstanceId']} ({volume['Attachments'][0]['Device']})")

  # Get AMI IDs
  #amis = ec2.get_ami_id()
  #print(dumps(amis, indent=2))
  
  # Get ECR repository images
  ecr.print_repo_images(repo_filter='tools/ci-env', tag_filter="^v[0-9]+.[0-9]+.*")

  # Get ECR repository config
  #repo_config = ecr.get_repo_config(repo_name='lokalise-main/app')
  #print(dumps(repo_config, indent=2))

  # Modify the ECR repository policy of all repos matching the filter
  #ecr.batch_mod_repo_policy_statement_arns(
  #  repo_filter="okapi-wrapper/.*",
  #  arns=[
  #    "arn:aws:iam::632374391739:user/stage-lok-app-main",
  #    "arn:aws:iam::046350321864:user/live-lok-app-main"
  #  ],
  #  statement_sid='AllowCrossAccountRO',
  #  replace=False,
  #  dry_run=True
  #)

  # Modify the ECR repository lifecycle policy of all repos matching the filter
  #repos = ecr.get_repo_names(filter='lokalise-main/.*')
  #for repo in repos:
  #  print(f"Modifying lifecycle policy for {repo}")
  #  lifecycle_policy = loads(ecr.get_lifecycle_policy(repo))
  #  lifecycle_policy['rules'][0]['selection']['countNumber'] = 100
  #  result = ecr.mod_lifecycle_policy(repo, dumps(lifecycle_policy))
  #  if result:
  #    print(f"Successfully modified lifecycle policy for {repo}")
  #  else:
  #    print(f"Failed to modify lifecycle policy for {repo}")

  # Get SNS topics
  #topics = sns.get_sns_topics(filter='.*autopilot-.*')
  #for topic in topics:
  #  print(f"Topic: {topic}")
  #  subscriptions = sns.get_sns_topic_subscriptions(topic)
  #  for subscription in subscriptions:
  #    print(f"  Subscription: {subscription[1]} -> {subscription[2]}")

  # Get Route53 Hosted Zones
  #zones = route53.get_zone_by_name(name_pattern='lokalise.com', private=True)
  #for z in zones:
  #  print(f"Zone: {z['Name']} ({z['Id']})")
  #  records = route53.get_zone_records(z['Id'], name_pattern='review-center-.*')
  #  for r in records:
  #    print(f"  Record: {r['Name']} ({r['Type']} {r['TTL']}) -> {r['ResourceRecords'][0]['Value']}")