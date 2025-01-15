import json
import boto3
import base64
import os

# Initialize the S3 client
s3_client = boto3.client('s3')

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

def lambda_handler(event, context):
    try:
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'body': json.dumps('Request body is required.')
            }

        body = json.loads(event['body'])

        file_content_base64 = body.get('file')
        file_name = body.get('fileName')

        if not file_content_base64 or not file_name:
            return {
                'statusCode': 400,
                'body': json.dumps('Both file and fileName are required in the request.')
            }

        file_content = base64.b64decode(file_content_base64)

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content,
            ContentType='application/pdf' if file_name.endswith('.pdf') else 'application/octet-stream'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f'File {file_name} uploaded successfully to bucket {BUCKET_NAME}.')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }
