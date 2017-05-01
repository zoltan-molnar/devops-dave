import logging
import json
from datetime import datetime
from utils import dynamodb, kms


user_configs_table = dynamodb.Table('user-configs')


def get(item_id):
    item = user_configs_table.get_item(Key={'id': item_id}).get('Item', {})
    logging.info('Get user-configs. ID: %s item: %s', item_id, item)
    if not item:
        return {}
    encrypted_config = item.get('config')
    if encrypted_config:
        item['config'] = json.loads(kms.decrypt(encrypted_config))
    else:
        item['config'] = {}
    return item


def update(item_id, params):
    update_expression = '''
    SET
        created_at = if_not_exists(created_at, :created_at),
        updated_at = :updated_at,
        last_modified_by = :last_modified_by,
        config = :config
    '''
    logging.info('Update user-configs. ID: %s params: %s', item_id, params)
    return user_configs_table.update_item(
        Key={'id': item_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues={
            ':updated_at': str(datetime.utcnow()),
            ':created_at': str(datetime.utcnow()),
            ':last_modified_by': params['last_modified_by'],
            ':config': kms.encrypt(json.dumps(params['config']))
        },
        ReturnValues='ALL_NEW'
    ).get('Attributes')
