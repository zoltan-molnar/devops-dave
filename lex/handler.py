import logging
from importlib import import_module


def handler(event):
    logging.info('Incoming Lex message: %s', str(event))

    sources = {
        'DialogCodeHook': 'dialog',
        'FulfillmentCodeHook': 'fulfillment',
    }

    event['sessionAttributes'] = event['sessionAttributes'] if event.get('sessionAttributes') else {}

    intent_name = event['currentIntent']['name']
    invocation_source = sources[event['invocationSource']]

    response = import_module('lex.%s.%s' % (intent_name, invocation_source)).handler(event)

    if invocation_source == 'fulfillment':
        response = after_fulfillment(response)

    logging.info('Lex response: %s', str(response))

    return response


def after_fulfillment(response):
    if response['sessionAttributes'] and response['sessionAttributes'].get('scheduling_status'):
        if response['sessionAttributes']['scheduling_status'] == 'scheduling':
            del response['sessionAttributes']['scheduling_status']
            del response['sessionAttributes']['scheduling_datetime']
        elif response['sessionAttributes']['scheduling_status'] == 'set_in_this_fulfillment':
            response['sessionAttributes']['scheduling_status'] = 'scheduling'

    return response
