import boto3

from alfred.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
