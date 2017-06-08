from lex.helpers import get_target, get_aws_client, aws_manager_decorator
from lex.responses import fulfill, get_slot


@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)
    if not target:
        return get_slot(event, 'target', 'missing_target')
    logs = get_aws_client('logs', aws_config)
    log_streams = logs.describe_log_streams(
        logGroupName=str(target),
        orderBy='LastEventTime',
        descending=True,
        limit=1
    )

    log = ''
    if log_streams and log_streams.get('logStreams') and log_streams['logStreams'][0]:
        log_stream = log_streams['logStreams'][0]['logStreamName']
        response = logs.get_log_events(
            logGroupName=str(target),
            logStreamName=log_stream,
            limit=25,
            startFromHead=False
        )

        for record in response.get('events'):
            log += record.get('message', '') + '\n'

    if not log:
        return fulfill(event, 'log_not_found')

    return fulfill(event, str(log), True)
