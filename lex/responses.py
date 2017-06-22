from random import randint
from utils import file


def get_response_by_response_code(lex_module, response_code):
    if not str(response_code):
        return ''
    global_responses = file.load_json_file('lex/global_responses')
    local_responses = file.load_json_file('lex/' + lex_module + '/responses')

    responses = global_responses.get(response_code, [])
    responses.extend(local_responses.get(response_code, []))

    if not responses or not len(responses):
        return ''

    random_number = randint(0, len(responses) - 1)

    return str(responses[random_number]) + '\n'


def get_response(lex_module, response_code='', custom_response=''):
    response = get_response_by_response_code(lex_module, response_code)
    response += str(custom_response)

    return response if response else 'Response is missing'


def get_slot(event, slot_name, response='', custom_response=''):
    return {
        'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': event['currentIntent']['name'],
            'slots': event['currentIntent']['slots'],
            'slotToElicit': slot_name,
            'message': {
                'contentType': 'PlainText',
                'content': get_response(event['currentIntent']['name'], response, custom_response)
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


def fulfill(event, response='success', custom_response=''):
    return {
        'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
              'contentType': 'PlainText',
              'content': get_response(event['currentIntent']['name'], response, custom_response)
            }
        }
    }


def deny(event, response='deny', custom_response=''):
    return {
        'sessionAttributes': event['sessionAttributes'] if event['sessionAttributes'] is not None else {},
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Failed',
            'message': {
              'contentType': 'PlainText',
              'content': get_response(event['currentIntent']['name'], response, custom_response)
            }
        }
    }


def confirm(event, response='confirm', custom_response=''):
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
                  'content': get_response(event['currentIntent']['name'], response, custom_response)
                }
            }
        }
