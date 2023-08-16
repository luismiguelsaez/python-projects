import ecr
from json import dumps, loads

if __name__ == "__main__":
  repos = ecr.get_ecr_repo_names(filter='languagetool')

  policy = ecr.get_ecr_repo_policy(repos[0])

  modded_policy = ecr.mod_policy_statement_arns(
    policy=loads(policy),
    statement_sid='AllowCrossAccountRO',
    arns=["arn:aws:iam::046350321864:role/lok-dummy-*","arn:aws:iam::046350321864:role/lok-dummy-2-*"],
    replace=False
  )

  print(dumps(modded_policy, indent=2))
  #ecr.set_ecr_repo_policy(repos[0], dumps(modded_policy))