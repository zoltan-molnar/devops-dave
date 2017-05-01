from lex.helpers import get_namespace
from lex.responses import validate_aws_config, get_slot


def handler(event):
    event['currentIntent']['slots']['namespace'] = get_namespace(event['currentIntent']['slots']['namespace'])

    if not event['currentIntent']['slots']['alias']:
        return get_slot(event, 'alias', 'alias')

    if not event['currentIntent']['slots']['target']:
        return get_slot(event, 'target', 'target')

    return validate_aws_config(event)
