import boto3
import re
from json import loads, dumps

session = boto3.Session()
ecr_client = session.client('ecr')

def get_ecr_repo_names(filter: str = None)->list[str]:
    repos = ecr_client.describe_repositories()
    if filter is None:
      return [ r['repositoryName'] for r in repos['repositories'] ]
    else:
      return [ r['repositoryName'] for r in repos['repositories'] if re.match(filter, r['repositoryName']) ]

def get_ecr_repo_policy(repo_name: str)->str:
    policy = ecr_client.get_repository_policy(repositoryName=repo_name)
    return policy['policyText']

def set_ecr_repo_policy(repo_name:str, policy:str)->None:
    response = ecr_client.set_repository_policy(repositoryName=repo_name, policyText=policy)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
      return False
    return True

def mod_policy_statement_arns(policy: dict, statement_sid: str, arns: list[str])->dict:
  """
  This is a very specific use case where the ECR policy uses a `StringLike` condition to allow access to a specific set of ARNs
  """
  statement_body = None
  statement_idx = None

  for s in range(len(policy['Statement'])):
    if policy['Statement'][s]["Sid"] == statement_sid:
      statement_body = policy['Statement'][s]
      statement_idx = s

  if statement_idx is None:
    return None

  allowed_arns = statement_body['Condition']['StringLike']['aws:PrincipalArn']

  modded_statement = statement_body
  modded_statement['Condition']['StringLike']['aws:PrincipalArn'] = allowed_arns + arns

  del policy['Statement'][statement_idx]
  policy['Statement'].append(modded_statement)

  return policy
