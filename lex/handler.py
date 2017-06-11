import logging
from importlib import import_module


def handler(event):
    logging.info('Incoming Lex message: %s', str(event))

    sources = {
        'DialogCodeHook': 'dialog',
        'FulfillmentCodeHook': 'fulfillment',
    }

    event['sessionAttributes'] = event['sessionAttributes'] if event['sessionAttributes'] else {}

    intent_name = event['currentIntent']['name']
    invocation_source = sources[event['invocationSource']]

    response = import_module('lex.%s.%s' % (intent_name, invocation_source)).handler(event)

    return response
