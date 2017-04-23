from importlib import import_module


def handler(event):
    sources = {
        'DialogCodeHook': 'dialog',
        'FulfillmentCodeHook': 'fulfillment',
    }

    intent_name = event['currentIntent']['name']
    invocation_source = sources[event['invocationSource']]

    return import_module('lex.%s.%s' % (intent_name, invocation_source)).handler(event)
