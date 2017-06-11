from lex.helpers import get_target, get_aws_resource, aws_manager_decorator, schedule_if_needed
from lex.responses import fulfill, get_slot


@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)
    if not target:
        return get_slot(event, 'target', 'missing_target')

    scheduled = schedule_if_needed(event, {'target': target})
    if scheduled:
        return scheduled

    action(aws_config, {'target': target})

    return fulfill(event, 'success')


def action(aws_config, params):
    ec2 = get_aws_resource('ec2', aws_config)
    instance = ec2.Instance(str(params['target']))

    instance.reboot()
