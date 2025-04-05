import boto3
import os
import sys
import uuid
import json
from PIL import Image
import PIL.Image
import urllib.parse
     
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
     
def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)
     
def lambda_handler(event, context):
    # Get SNS topic ARN from environment variable
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    if not sns_topic_arn:
        print("Error: SNS_TOPIC_ARN environment variable not set")
        return {
            'statusCode': 500,
            'body': 'SNS_TOPIC_ARN environment variable not configured'
        }
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)
        
        try:
            # Download the image
            s3_client.download_file(bucket, key, download_path)
            
            # Resize the image
            resize_image(download_path, upload_path)
            
            # Upload the resized image
            s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key)
            
            # Publish success message to SNS topic
            message = {
                'bucket': bucket,
                'key': key,
                'resized_bucket': '{}-resized'.format(bucket),
                'status': 'success'
            }
            
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(message),
                Subject='Image Resize Notification - Success'
            )
            
        except Exception as e:
            # Publish error message to SNS topic
            error_message = {
                'bucket': bucket,
                'key': key,
                'status': 'error',
                'error': str(e)
            }
            
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=json.dumps(error_message),
                Subject='Image Resize Notification - Error'
            )
            
            print(f"Error processing {bucket}/{key}: {str(e)}")
            
        finally:
            # Clean up temporary files
            if os.path.exists(download_path):
                os.remove(download_path)
            if os.path.exists(upload_path):
                os.remove(upload_path)
