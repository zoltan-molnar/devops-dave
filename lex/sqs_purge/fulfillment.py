from lex.helpers import get_aws_config
from lex.responses import fulfill


def handler(event):
    config = get_aws_config(event['userId'])
    print('config %s' % str(config))
    return fulfill(event, 'success')
