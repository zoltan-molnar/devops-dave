from lex.helpers import delegate


def handler(event):
    keys = ['aws_access_key', 'aws_secret_key', 'aws_region']

    # remove old data
    for key in keys:
        if event['sessionAttributes'].get('new_' + key):
            del event['sessionAttributes']['new_' + key]

    return delegate(event)
