from lex.helpers import get_response, get_aws_config, validate_aws_config


def handler(event):
    config = get_aws_config(event['userId'])
    print('config %s' % str(config))
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            "message": {
              "contentType": "PlainText",
              "content": get_response('sqs_purge', 'success')
            },
        }
    }
