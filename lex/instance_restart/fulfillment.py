from lex.helpers import get_target, get_aws_resource, aws_manager_decorator, can_be_scheduled_decorator
from lex.responses import fulfill, get_slot


@can_be_scheduled_decorator
@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)

    ec2 = get_aws_resource('ec2', aws_config)
    instance = ec2.Instance(str(target))

    instance.reboot()

    return fulfill(event, 'success')
