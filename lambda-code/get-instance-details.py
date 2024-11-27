import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    ec2 = boto3.client('ec2')
    instance_id = event.get('instance_id')

    if not instance_id:
        print("Error: No instance_id provided in the event")
        return {
            'statusCode': 400,
            'body': json.dumps('Error: instance_id is required')
        }

    try:
        print(f"Describing instance: {instance_id}")
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        volume_id = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']

        print(f"Describing volume: {volume_id}")
        volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
        current_size = volume_response['Volumes'][0]['Size']

        result = {
            'instance_id': instance_id,
            'volume_id': volume_id,
            'current_size': current_size
        }
        print(f"Result: {json.dumps(result)}")
        return result

    except ClientError as e:
        print("error fetching details(client error)", e)
