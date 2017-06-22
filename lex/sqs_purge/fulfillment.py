from lex.helpers import get_target, get_aws_client, aws_manager_decorator, can_be_scheduled_decorator
from lex.responses import fulfill, get_slot


@can_be_scheduled_decorator
@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)
    sqs_client = get_aws_client('sqs', aws_config)

    sqs_client.purge_queue(QueueUrl=target)
    return fulfill(event, 'success')
