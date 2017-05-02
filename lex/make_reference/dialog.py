import logging
from lex.responses import delegate, get_slot


def handler(event):

    logging.info('alias %s', event['currentIntent']['slots']['alias'])
    logging.info('target %s', event['currentIntent']['slots']['target'])

    if not event['currentIntent']['slots']['alias']:
        return get_slot(event, 'alias', 'alias')

    if not event['currentIntent']['slots']['target']:
        return get_slot(event, 'target', 'target')

    return delegate(event)
