import boto3
import re
from json import loads, dumps

session = boto3.Session()
ecr_client = session.client('ecr')

def get_repo_names(filter: str)->list[str]:
    repos = ecr_client.describe_repositories()
    return [ r['repositoryName'] for r in repos['repositories'] if re.match(filter, r['repositoryName']) ]

def get_repo_policy(repo_name: str)->str:
    policy = ecr_client.get_repository_policy(repositoryName=repo_name)
    return policy['policyText']

def get_lifecycle_policy(repo_name: str)->str:
    policy = ecr_client.get_lifecycle_policy(repositoryName=repo_name)
    return policy['lifecyclePolicyText']

def set_repo_policy(repo_name:str, policy:str)->bool:
    response = ecr_client.set_repository_policy(repositoryName=repo_name, policyText=policy)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
      return False
    return True

def mod_lifecycle_policy(repo_name:str, policy:str)->bool:
    response = ecr_client.put_lifecycle_policy(repositoryName=repo_name, lifecyclePolicyText=policy)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
      return False
    return True

def get_repo_images(repo_name: str, sort: bool = True)->list[dict]:
    images = ecr_client.describe_images(repositoryName=repo_name)
    if sort:
      return sorted(images['imageDetails'], key=lambda k: k['imagePushedAt'], reverse=False)
    return images['imageDetails']

def get_repo_image_tags(repo_name: str, filter: str = ".*")->dict[str, dict[str, list[str]]]:
    images = ecr_client.describe_images(repositoryName=repo_name)
    filtered_images = {}
    for image in sorted(images['imageDetails'], key=lambda k: k['imagePushedAt'], reverse=False):
      if 'imageTags' in image:
        push_date = image['imagePushedAt'].strftime("%Y-%m-%d %H:%M:%S")
        digest = image['imageDigest']
        size = image['imageSizeInBytes']
        filtered_tags = [ t for t in image['imageTags'] if re.match('^[0-9]+$', t) ]
        if len(filtered_tags) > 0:
          filtered_images[digest] = {
            'push_date': push_date,
            'size': size,
            'tags': filtered_tags
          }

    return filtered_images

def print_repo_images(repo_filter: str = '.*', tag_filter: str = ".*")->None:
  repos = get_repo_names(filter=repo_filter)
  for repo in repos:
    images = get_repo_image_tags(repo, filter=tag_filter)
    if len(images) > 0:
      print(f"Repo: {repo}")
      for image in images:
        print("[{}] {:10.0f} {} {}".format(images[image]['push_date'], images[image]['size'], image, ",".join(images[image]['tags'])))

def batch_mod_repo_policy_statement_arns(repo_filter: str, arns: list[str], statement_sid: str = 'AllowCrossAccountRO', replace: bool = False, dry_run: bool = True)->None:
  repos = get_repo_names(filter=repo_filter)
  for repo in repos:
    policy = get_repo_policy(repo)
    modded_policy = mod_repo_policy_statement_arns(
      policy=loads(policy),
      statement_sid=statement_sid,
      arns=arns,
      replace=replace
    )
    if dry_run:
      print(f"-> Would have modified policy for {repo} to this\n")
      print(dumps(modded_policy, indent=2))
    else:
      if set_repo_policy(repo, dumps(modded_policy)):
        print(f"Successfully modified policy for {repo}")
      else:
        print(f"Failed to modify policy for {repo}: {dumps(modded_policy)}")

def mod_repo_policy_statement_arns(policy: dict, statement_sid: str, arns: list[str], replace: bool = False)->dict:
  """
  This is a very specific use case where the ECR policy uses a `StringLike` condition to allow access to a specific set of ARNs
  """
  statement_idx = None

  for s in range(len(policy['Statement'])):
    if policy['Statement'][s]["Sid"] == statement_sid:
      statement_idx = s

  if replace:
    policy['Statement'][statement_idx]['Condition']['StringLike']['aws:PrincipalArn'] = arns
  else:
    allowed_arns = policy['Statement'][statement_idx]['Condition']['StringLike']['aws:PrincipalArn']
    policy['Statement'][statement_idx]['Condition']['StringLike']['aws:PrincipalArn'] = allowed_arns + arns

  return policy
