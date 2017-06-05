from lex.helpers import get_target, get_aws_client, aws_manager_decorator
from lex.responses import fulfill


@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)
    sqs_client = get_aws_client('sqs', aws_config)

    sqs_client.purge_queue(QueueUrl=target)
    return fulfill(event, 'success')
