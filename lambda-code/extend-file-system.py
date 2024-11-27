import boto3

def lambda_handler(event, context):
    ssm = boto3.client('ssm')

    instance_id = event['instance_id']

    # command for ubuntu 22.04 with lvm
    command = "sudo growpart /dev/xvda 1 && sudo resize2fs /dev/xvda1"

    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': [command]}
    )

    return {
        'instance_id': instance_id,
        'command_id': response['Command']['CommandId']
    }
