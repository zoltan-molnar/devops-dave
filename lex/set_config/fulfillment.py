from lex.helpers import get_namespace, get_id
from lex.responses import fulfill, confirm
from models import user_config


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

    return fulfill(event, 'success')

