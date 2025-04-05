import boto3
import json
import os
import urllib.parse
from io import BytesIO
from PIL import Image

# Environment variables
SOURCE_BUCKET = os.environ['SOURCE_BUCKET']
DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

# Target size for resizing (width, height)
TARGET_WIDTH = int(os.environ.get('TARGET_WIDTH', 800))
TARGET_HEIGHT = int(os.environ.get('TARGET_HEIGHT', 600))

# Initialize AWS clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Log the event received
    print("Received event: " + json.dumps(event))
    
    try:
        # Get the object from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        # Validate source bucket
        if bucket != SOURCE_BUCKET:
            raise Exception(f"Incorrect source bucket. Expected: {SOURCE_BUCKET}, Received: {bucket}")
        
        # Check if the file is an image based on extension
        if not key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
            print(f"File {key} is not a supported image type. Skipping.")
            return {
                'statusCode': 200,
                'body': json.dumps(f"File {key} is not a supported image type. Skipping.")
            }
        
        # Download the image from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        image_content = response['Body'].read()
        
        # Process the image
        result = resize_image(image_content, key)
        
        # Publish to SNS
        message = {
            'status': 'SUCCESS',
            'processing_details': {
                'original_image': {
                    'bucket': bucket,
                    'key': key
                },
                'resized_image': {
                    'bucket': DESTINATION_BUCKET,
                    'key': result['key'],
                    'dimensions': {
                        'width': result['dimensions'][0],
                        'height': result['dimensions'][1]
                    }
                }
            },
            'timestamp': context.get_remaining_time_in_millis()
        }
        
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Image Processing Complete: {key}",
            Message=json.dumps(message, indent=2),  
            MessageStructure='string'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully processed {key} and created resized version")
        }
        
    except Exception as e:
        print(f"Error processing {key}: {str(e)}")
        
        # Publish error to SNS
        error_message = {
            'status': 'ERROR',
            'error_details': {
                'error_message': str(e),
                'image_info': {
                    'bucket': bucket if 'bucket' in locals() else 'Unknown',
                    'key': key if 'key' in locals() else 'Unknown'
                }
            },
            'timestamp': context.get_remaining_time_in_millis()
        }
        
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Image Processing Error: {key if 'key' in locals() else 'Unknown'}",
            Message=json.dumps(error_message, indent=2),  # Add indent for pretty formatting
            MessageStructure='string'
        )
        
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing image: {str(e)}")
        }

def resize_image(image_content, key):
    """
    Resize the image to the target size and upload to destination bucket
    """
    try:
        # Open the image using PIL
        with Image.open(BytesIO(image_content)) as img:
            # Get file name and extension
            file_name, file_ext = os.path.splitext(os.path.basename(key))
            
            # Create a copy of the image to resize
            img_copy = img.copy()
            
            # Convert mode if needed
            if img_copy.mode not in ('RGB', 'RGBA'):
                img_copy = img_copy.convert('RGB')
            
            # Resize the image while preserving aspect ratio
            img_copy.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
            
            # Prepare the resized image for upload
            buffer = BytesIO()
            img_copy.save(buffer, format=img.format if img.format else 'JPEG')
            buffer.seek(0)
            
            # Create the new key for the resized image
            resized_key = f"resized/{file_name}{file_ext}"
            
            # Upload the resized image to the destination bucket
            s3_client.put_object(
                Body=buffer,
                Bucket=DESTINATION_BUCKET,
                Key=resized_key,
                ContentType=f"image/{img.format.lower() if img.format else 'jpeg'}"
            )
            
            # Return information about the resized image
            return {
                'dimensions': img_copy.size,
                'key': resized_key
            }
                
    except Exception as e:
        print(f"Error resizing image: {str(e)}")
        raise