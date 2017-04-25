from lex.helpers import get_response


def handler(event):
    response = get_response('sqs_purge', 'success')
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            "message": {
              "contentType": "PlainText",
              "content": response
            },
        }
    }
