from lex.helpers import delegate
import logging


def handler(event):
    keys = ['aws_access_key', 'aws_secret_key', 'aws_region']

    logging.info('Removing old config')

    # Let's get the namespace first.
    if not event['currentIntent']['slots'].get('reseted') or event['currentIntent']['slots']['reseted'] != 'yes':
        # remove old data
        event['currentIntent']['slots']['reseted'] = 'yes'
        for key in keys:
            if event['sessionAttributes'].get('new_' + key):
                del event['sessionAttributes']['new_' + key]

    return delegate(event)
