import boto3
import re

session = boto3.Session()
sns_client = session.client('sns')

def get_sns_topics(filter: str = '.*')->list[str]:
    topics = sns_client.list_topics()
    return [ t['TopicArn'] for t in topics['Topics'] if re.match(filter, t['TopicArn']) ]

def get_sns_topic_subscriptions(topic_arn: str)->list[tuple[str,str,str]]:
    subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    return [ (s['SubscriptionArn'], s['Protocol'], s['Endpoint']) for s in subscriptions['Subscriptions'] ]
