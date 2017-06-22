import logging
from lex import handler as lex_handler


def lex(event, context):
    logging.debug('lex event: %s' % event)
    return lex_handler.handler(event)


def worker_test(event, context):
    logging.debug('worker_test event: %s' % event)
    return {}


def execute_lex_scheduled_action(event, context):
    logging.debug('execute_lex_scheduled_action event: %s' % event)
    return {}


def schedule_lex_actions(event, context):
    logging.debug('schedule_lex_actions event: %s' % event)
    return {}
