from lex.helpers import get_namespace, get_id
from lex.responses import fulfill, confirm, get_slot
from models import user_config


def handler(event):
    keys = ['aws_access_key', 'aws_secret_key', 'aws_region']

    # Let's get the namespace first.
    event['currentIntent']['slots']['namespace'] = get_namespace(event['currentIntent']['slots']['namespace'])
    if not event['currentIntent']['slots']['namespace']:
        # remove old data
        for key in keys:
            if event['sessionAttributes'].get('new_' + key):
                del event['sessionAttributes']['new_' + key]

        return get_slot(event, 'namespace', 'missing_namespace')

    # Copy the config into session attributes, but add a new_ prefix, so it won't affect the current config
    for key in keys:
        if event['currentIntent']['slots'].get(key):
            event['sessionAttributes']['new_' + key] = event['currentIntent']['slots'][key]

    # check for missing data
    for key in keys:
        if not event['sessionAttributes'] or not event['sessionAttributes'].get('new_' + key):
            return get_slot(event, key, 'missing_' + key)

    item_id = get_id(event)
    item = user_config.get(item_id)

    if item:
        response = confirm(event)
        if response:
            return response

    config = {
        'namespace': event['currentIntent']['slots']['namespace'],
        'aws_access_key': event['sessionAttributes']['new_aws_access_key'],
        'aws_secret_key': event['sessionAttributes']['new_aws_secret_key'],
        'aws_region': event['sessionAttributes']['new_aws_region']
    }

    del event['sessionAttributes']['new_aws_access_key']
    del event['sessionAttributes']['new_aws_secret_key']
    del event['sessionAttributes']['new_aws_region']

    # Insert or update config record
    user_config.update(item_id, {
        'last_modified_by': event['userId'],
        'config': config
    })

    return fulfill(event, 'success')

