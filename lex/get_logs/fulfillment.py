import logging

from lex.helpers import get_target, get_aws_client, aws_manager_decorator
from lex.responses import fulfill


@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)
    logs = get_aws_client('logs', aws_config)
    response = logs.filter_log_events(
        logGroupName=str(target),
        limit=25
    )

    logging.info(response.get('events'))

    log = ''
    for record in response.get('events'):
        log += record.get('message', '') + '\n'

    return fulfill(event, str(log), True)
