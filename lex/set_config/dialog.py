from lex.helpers import validate_aws_config, get_response, get_namespace


def handler(event):
    event['currentIntent']['slots']['namespace'] = get_namespace(event['currentIntent']['slots']['namespace'])
    if not event['currentIntent']['slots']['namespace']:
        return {
            'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': event['currentIntent']['slots'],
                'slotToElicit': 'namespace',
                'message': {
                    'contentType': 'PlainText',
                    'content': get_response(event['currentIntent']['name'], 'missing_namespace')
                }
            }
        }

    return validate_aws_config(event)
