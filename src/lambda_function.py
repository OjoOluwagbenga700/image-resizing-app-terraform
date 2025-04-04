import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import json
     
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)
     
def lambda_handler(event, context):
    # Get SNS topic ARN from environment variable
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key'] 
            download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
            upload_path = '/tmp/resized-{}'.format(key)
            
            # Download, resize and upload
            s3_client.download_file(bucket, key, download_path)
            resize_image(download_path, upload_path)
            destination_bucket = '{}-resized'.format(bucket)
            s3_client.upload_file(upload_path, destination_bucket, key)
            
            # Prepare and send SNS notification
            message = {
                'status': 'success',
                'original_image': {
                    'bucket': bucket,
                    'key': key
                },
                'thumbnail': {
                    'bucket': destination_bucket,
                    'key': key
                }
            }
            
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=str(message),
                Subject='Image Processing Completed'
            )

        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(message)
        }
            
    except Exception as e:
        error_message = {
            'status': 'error',
            'error': str(e),
            'image': {
                'bucket': bucket,
                'key': key
            }
        }
        # Publish error notification
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=str(error_message),
            Subject='Image Processing Error'
        )

        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(error_message)
        }
