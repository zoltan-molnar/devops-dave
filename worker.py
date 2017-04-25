import logging
from lex import handler as lex_handler


def lex(event, context):
    logging.debug('lex event: %s' % event)
    return lex_handler.handler(event)


def worker_test(event, context):
    logging.debug('worker_test event: %s' % event)
    return {}
