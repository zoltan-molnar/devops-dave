from lex.helpers import get_target, get_aws_client, aws_manager_decorator, can_be_scheduled_decorator
from lex.responses import fulfill, get_slot


@can_be_scheduled_decorator
@aws_manager_decorator
def handler(event, aws_config):
    target = str(get_target(event))

    # there is a strange bug, that AWS Lex sometimes cuts down the first / char
    # this should solve it
    if target and target[0:1] != '/':
        target = '/' + target

    limit = 25
    if event['currentIntent']['slots'].get('limit'):
        limit = int(event['currentIntent']['slots']['limit'])

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
            limit=limit,
            startFromHead=False
        )

        for record in response.get('events'):
            log += record.get('message', '') + '\n'

    if not log:
        return fulfill(event, 'log_not_found')

    return fulfill(event, None, str(log))
