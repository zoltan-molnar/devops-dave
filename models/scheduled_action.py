import logging
from uuid import uuid4
from datetime import datetime
from utils import dynamodb
from boto3.dynamodb.conditions import Attr

table = dynamodb.Table('scheduled-actions')


def get(item_id):
    item = table.get_item(Key={'id': item_id}).get('Item', {})
    logging.info('Get user-configs. ID: %s item: %s', item_id, item)

    return item if item else {}


def add(params):
    item_id = str(uuid4())
    update_expression = '''
    SET
        created_at = :created_at,
        updated_at = :updated_at,
        added_by = :added_by,
        event = :event,
        execution_status = :execution_status,
        scheduled_datetime = :scheduled_datetime
    '''
    logging.info('Add new scheduled-actions.params: %s', str(params))
    return table.update_item(
        Key={'id': item_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues={
            ':created_at': str(datetime.utcnow()),
            ':updated_at': str(datetime.utcnow()),
            ':added_by': params['added_by'],
            ':event': params['event'],
            ':execution_status': params['execution_status'],
            ':scheduled_datetime': params['scheduled_datetime']
        },
        ReturnValues='ALL_NEW'
    ).get('Attributes')


def list_for_scheduling():
    return table.query(
        ScanIndexForward=True,
        FilterExpression=Attr('execution_status').eq('not_started').__and__(
            Attr('scheduled_time').lte(str(datetime.utcnow()))
        )
    )


def update_status(item_id, new_status):
    update_expression = '''
    SET
        updated_at = :updated_at,
        execution_status = :execution_status
    '''
    logging.info('scheduled_action.update_status:\nid: %s\nnew_status: %s', str(item_id), str(new_status))
    return table.update_item(
        Key={'id': item_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues={
            ':updated_at': str(datetime.utcnow()),
            ':execution_status': new_status
        },
        ReturnValues='ALL_NEW'
    ).get('Attributes')
