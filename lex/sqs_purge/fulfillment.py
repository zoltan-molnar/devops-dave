def handler(event):
    print('event:')
    print(event)
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled'
        }
    }
