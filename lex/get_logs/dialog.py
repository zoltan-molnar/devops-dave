from lex.helpers import validate_aws_config
from lex.responses import get_slot


def handler(event):
    if not event['currentIntent']['slots'].get('target'):
        return get_slot(event, 'target', 'missing_target')
    return validate_aws_config(event)
