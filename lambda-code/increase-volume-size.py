import boto3
import math

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    volume_id = event['volume_id']
    current_size = event['current_size']

    # Calculate new size (5GB increase)
    new_size = math.ceil(current_size + 5)

    print(f"Increasing volume from {current_size} GB to {new_size} GB")

    try:
        response = ec2.modify_volume(
            VolumeId=volume_id,
            Size=new_size
        )

        print(f"Volume modification initiated: {response['VolumeModification']}")

        result = {
            'volume_id': volume_id,
            'original_size': current_size,
            'new_size': new_size
        }
        return result

    except Exception as e:
        print(f"Error modifying volume: {str(e)}")
        raise e
