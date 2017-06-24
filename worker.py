import logging
from zappa.async import run
from lex import handler as lex_handler
from models.scheduled_action import list_for_scheduling, update_status
from utils.config import CONFIG


def lex(event, context):
    logging.info('lex event: %s' % event)
    return lex_handler.handler(event)


def execute_lex_scheduled_action(event, context):
    logging.info('execute_lex_scheduled_action event: %s' % event)
    result = list_for_scheduling()
    for action in result:
        if not CONFIG.get('local'):
            run(schedule_lex_actions, [action, {}], {}, service='sns')
        else:
            schedule_lex_actions(action, {})

    logging.info('execute_lex_scheduled_action list_for_scheduling: %s' % str(result))
    return result


def schedule_lex_actions(event, context):
    logging.info('schedule_lex_actions event: %s' % event)
    event['event']['sessionAttributes'] = {
        'scheduling_status': 'processing',
    }
    response = lex_handler.handler(event['event'])
    update_status(event['id'], 'processed')
    logging.info('schedule_lex_actions response: %s' % response)
    return response
