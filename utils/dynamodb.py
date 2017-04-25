import boto3
from utils.config import CONFIG
import logging

dynamodb = boto3.resource('dynamodb', region_name=CONFIG['aws_region'])


def Table(table_name):
    table_full_name = '-'.join((CONFIG['project'], CONFIG['env'], table_name))
    logging.info('Loading DynamoDB table: %s', table_full_name)
    return dynamodb.Table(table_full_name)
