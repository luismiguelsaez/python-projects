import ecr, sns, route53
from json import dumps, loads
import re

if __name__ == "__main__":

  # Get ECR repository images
  repos = ecr.get_repo_names(filter='okapi-wrapper/.*')
  for repo in repos:
    print(f"Repo: {repo}")
    images = ecr.get_repo_image_tags(repo, filter='^[0-9]+$')
    for image in images:
      print(f"  - {image} ({images[image]['push_date']}) -> {images[image]['tags']}")

  # Modify the ECR repository policy
  #policy = ecr.get_repo_policy(repos[0])
  #modded_policy = ecr.mod_repo_policy_statement_arns(
  #  policy=loads(policy),
  #  statement_sid='AllowCrossAccountRO',
  #  arns=["arn:aws:iam::046350321864:role/lok-dummy-*","arn:aws:iam::046350321864:role/lok-dummy-2-*"],
  #  replace=False
  #)
  #print(dumps(modded_policy, indent=2))
  #ecr.set_repo_policy(repos[0], dumps(modded_policy))

  # Modify the ECR repository lifecycle policy
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