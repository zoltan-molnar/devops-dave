from random import randint
from utils import file
from models import user_config
from lex.helpers import get_aws_config


def get_response(lex_module, response_type):
    global_responses = file.load_json_file('lex/global_responses')
    local_responses = file.load_json_file('lex/' + lex_module + '/responses')

    responses = global_responses.get(response_type, [])
    responses.extend(local_responses.get(response_type, []))

    random_number = randint(0, len(responses) - 1)

    return responses[random_number]


def _get_missing_aws_config_name(config):
    required_keys = ['aws_access_key', 'aws_secret_key', 'aws_default_region']
    for required_key in required_keys:
        if not config or not config.get(required_key):
            return required_key
    return None


def validate_aws_config(event):
    config = get_aws_config(event['userId'])
    if _get_missing_aws_config_name(config):
        missing_config = _get_missing_aws_config_name(event['currentIntent']['slots'])
        if missing_config:
            return get_slot(event, missing_config, 'missing_' + missing_config)

        # Insert or update config record
        user_config.update(event['userId'], {
            'last_modified_by': event['userId'],
            'config': {
                'namespace': 'local',
                'aws_access_key': event['currentIntent']['slots']['aws_access_key'],
                'aws_secret_key': event['currentIntent']['slots']['aws_secret_key'],
                'aws_default_region': event['currentIntent']['slots']['aws_default_region']
            }
        })

    return delegate(event)


def get_slot(event, slot_name, response):
    return {
        'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': event['currentIntent']['name'],
            'slots': event['currentIntent']['slots'],
            'slotToElicit': slot_name,
            'message': {
                'contentType': 'PlainText',
                'content': get_response(event['currentIntent']['name'], response)
            }
        }
    }


def delegate(event):
    return {
        'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
        'dialogAction': {
            'type': 'Delegate',
            'slots': event['currentIntent']['slots']
        }
    }


def fulfill(event, response):
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
              'contentType': 'PlainText',
              'content': get_response(event['currentIntent']['name'], response)
            }
        }
    }


def deny(event, response):
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Failed',
            'message': {
              'contentType': 'PlainText',
              'content': get_response(event['currentIntent']['name'], response)
            }
        }
    }


def confirm(event):
    if event['currentIntent']['confirmationStatus'] == 'Denied':
        return deny(event, 'denied')

    if event['currentIntent']['confirmationStatus'] == 'None':
        return {
            'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
            'dialogAction': {
                'intentName': event['currentIntent']['name'],
                'slots': event['currentIntent']['slots'],
                'type': 'ConfirmIntent',
                'message': {
                  'contentType': 'PlainText',
                  'content': get_response(event['currentIntent']['name'], 'confirm')
                }
            }
        }
