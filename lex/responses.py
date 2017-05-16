from random import randint
from utils import file


def get_response(lex_module, response_type):
    global_responses = file.load_json_file('lex/global_responses')
    local_responses = file.load_json_file('lex/' + lex_module + '/responses')

    responses = global_responses.get(response_type, [])
    responses.extend(local_responses.get(response_type, []))

    random_number = randint(0, len(responses) - 1)

    return responses[random_number]


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


def deny(event, response, plain_text=''):
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Failed',
            'message': {
              'contentType': 'PlainText',
              'content': get_response(event['currentIntent']['name'], response) if not plain_text else plain_text
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
