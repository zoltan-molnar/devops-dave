from lex.helpers import aws_validator_decorator, get_target
from lex.responses import delegate, get_slot


@aws_validator_decorator
def handler(event):
    target = get_target(event)
    if not target:
        return get_slot(event, 'target', 'missing_target')
    return delegate(event)
