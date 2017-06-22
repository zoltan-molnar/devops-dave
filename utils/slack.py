import requests


def send_message_via_webhook(webhook, message):
    response = requests.post(webhook, data=message, headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError('Request to slack returned an error %s, the response is:\n%s' %
                         (response.status_code, response.text))

    return response
