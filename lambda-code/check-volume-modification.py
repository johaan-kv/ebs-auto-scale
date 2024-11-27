import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    volume_id = event['volume_id']


    response = ec2.describe_volumes_modifications(VolumeIds=[volume_id])
    print(f"response: {response}")

    if response['VolumesModifications']:
        modification = response['VolumesModifications'][0]
        modification_state = modification['ModificationState']
        print(modification_state)

        if modification_state == 'optimizing':
            return {
                'modificationComplete': False,
                'state': modification_state
            }
        elif modification_state == 'completed':
            return {
                'modificationComplete': True,
                'state': modification_state,
                'volume_id': volume_id
            }
        else:
            return {
                'modificationComplete': False,
                'state': modification_state
            }
    else:
        return {
            'modificationComplete': False,
            'state': 'unknown'
        }
