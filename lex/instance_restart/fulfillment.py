from lex.helpers import get_target, get_aws_client, aws_manager_decorator
from lex.responses import fulfill


@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)
    ec2_client = get_aws_client('ec2', aws_config)
    instance = ec2_client.Instance(target)

    instance.reboot()
    return fulfill(event, 'success')
