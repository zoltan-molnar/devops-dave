from lex.responses import get_slot
from lex.helpers import get_namespace, validate_aws_config


def handler(event):
    event['currentIntent']['slots']['namespace'] = get_namespace(event['currentIntent']['slots']['namespace'])
    if not event['currentIntent']['slots']['namespace']:
        return get_slot(event, 'namespace', 'missing_namespace')

    return validate_aws_config(event)
