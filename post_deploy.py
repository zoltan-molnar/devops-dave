from utils.config import CONFIG
import uuid

import boto3

client = boto3.client('lambda', region_name=CONFIG['aws_region'])

response = client.add_permission(
    FunctionName='devops-dave-production',
    StatementId=str(uuid.uuid4()),
    Action='lambda:InvokeFunction',
    Principal='lex.amazonaws.com',
    SourceArn='arn:aws:lex:us-east-1:680699795098:*'
)
