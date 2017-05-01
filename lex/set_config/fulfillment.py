import logging
from lex.lex_utils import get_team_id, get_user_id
from lex.helpers import get_namespace, get_response, confirm
from models import user_config


def get_id(event):
    namespace = event['currentIntent']['slots']['namespace']

    if namespace == 'global':
        return get_team_id(event['userId'])
    elif namespace == 'local':
        return get_user_id(event['userId'])

    raise StandardError('WRONG_NAMESPACE')


def handler(event):
    # Parsing namespace so we can accept multiple values like "team" or "my"
    event['currentIntent']['slots']['namespace'] = get_namespace(event['currentIntent']['slots']['namespace'])

    item_id = get_id(event)
    item = user_config.get(item_id)

    if item:
        response = confirm(event)
        if response:
            return response

    # Insert or update config record
    user_config.update(item_id, {
        'last_modified_by': event['userId'],
        'config': event['currentIntent']['slots']
    })

    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
              'contentType': 'PlainText',
              'content': get_response('set_config', 'success')
            }
        }
    }

