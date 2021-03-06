import boto3
import urllib.request
import json

region = 'xxxxxxxxxxxx'
instances = ['xxxxxxxxxxx']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    result = ec2.describe_instances(InstanceIds=instances)
    if("PublicIpAddress" in result['Reservations'][0]['Instances'][0]):
        comment = {"content": result['Reservations'][0]['Instances'][0]['PublicIpAddress']}
    else:
        comment = {"content": "パブリックIPアドレスが取得できませんでした。"}
    headers = {'content-type': 'application/json'}
    // webhook url
    url = 'xxxxxxxx'
    req = urllib.request.Request(
        url,
        json.dumps(comment).encode(),
        {"User-Agent": "curl/7.64.1", "Content-Type" : "application/json"},
        headers
    )
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
            print(body)
    except urllib.error.HTTPError as e:
        if e.code >= 400:
            print(e.reason)
        else:
            print("something error")
    return {
        'statusCode': 200
    }
