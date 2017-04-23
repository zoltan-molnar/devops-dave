import logging
from lex import handler as lex_handler
logger = logging.getLogger('app')


def lex(event, context):
    logger.debug('lex event: %s' % event)
    return lex_handler.handler(event)


def worker_test(event, context):
    logger.debug('worker_test event: %s' % event)
    return {}
