import json
import boto3

def get_instance_id_from_ip(ip_address):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    print(f"EC2 response: {json.dumps(response, default=str)}") 
    if response['Reservations']:
        return response['Reservations'][0]['Instances'][0]['InstanceId']
    return None

def lambda_handler(event, context):
    print("received alarm:", json.dumps(event))

    # extract alarm info
    alarm_name = event['alarmData']['alarmName']

    # extract hostname from dimension
    dimensions = event['alarmData']['configuration']['metrics'][0]['metricStat']['metric']['dimensions']
    instance_id = dimensions.get('InstanceId')
    print(instance_id)

    # start step function
    sf_client = boto3.client('stepfunctions')
    sf_arn = 'arn:aws:states:ap-south-1:402338187344:stateMachine:EBS-autoscale'  

    response = sf_client.start_execution(
        stateMachineArn=sf_arn,
        input=json.dumps({'instance_id': instance_id})
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'started scaling process for instance {instance_id}')
    }
