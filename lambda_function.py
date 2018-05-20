import json
import sys

import boto3

def get_event_details(event):
    data = json.loads(event['body'])
    tag = data['push_data']['tag']
    repo = data['repository']['repo_name']
    return repo, tag

def image_url(registry, repo, tag, protocol=None):
    url = '{}/{}'.format(registry, image_name(repo, tag))
    if protocol:
        return '{}://'.format(protocol, url)
    return url

def image_name(repo, tag):
    return '{}:{}'.format(repo, tag)

def lambda_handler(event, context):
    repo, tag = get_event_details(event)
    registry = 'index.docker.io'

    msg = {
	'image': image_name(repo, tag), 
	'registry': registry
    }

    print(msg)

    client = boto3.client('sns')

    rsp = client.publish(
	TopicArn=os.environ['SNS_ARN'],
	Message=json.dumps(msg)
    )

    print(rsp)

    return {} 


if __name__ == '__main__':
    lambda_handler(json.load(sys.stdin), {})
