import logging
from datetime import datetime
from utils import dynamodb


user_aliases_table = dynamodb.Table('user-aliases')


def get(item_id):
    item = user_aliases_table.get_item(Key={'id': item_id}).get('Item', {})
    logging.info('Get user-configs. ID: %s item: %s', item_id, item)

    return item if item else {}


def update(item_id, params):
    update_expression = '''
    SET
        created_at = if_not_exists(created_at, :created_at),
        updated_at = :updated_at,
        last_modified_by = :last_modified_by,
        aliases = :aliases
    '''
    logging.info('Update user-aliases. ID: %s params: %s', item_id, params)
    return user_aliases_table.update_item(
        Key={'id': item_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues={
            ':updated_at': str(datetime.utcnow()),
            ':created_at': str(datetime.utcnow()),
            ':last_modified_by': params['last_modified_by'],
            ':aliases': params['aliases']
        },
        ReturnValues='ALL_NEW'
    ).get('Attributes')
