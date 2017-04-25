import logging
from lex.lex_utils import get_team_id, get_user_id
from models import user_config


def get_id(event):
    namespace = event['currentIntent']['slots']['namespace']

    if namespace == 'global':
        return get_team_id(event['userId'])
    elif namespace == 'local':
        return get_user_id(event['userId'])

    raise StandardError('WRONG_NAMESPACE')


def handler(event):
    item_id = get_id(event)
    item = user_config.get(item_id)

    if item and False:  # TODO Check for confirmation
        pass
    # Insert or update config record
    user_config.update(item_id, {
        'last_modified_by': event['userId'],
        'config': event['currentIntent']['slots']
    })
    item = user_config.get(item_id)
    logging.info('item %s', item)
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled'
        }
    }

