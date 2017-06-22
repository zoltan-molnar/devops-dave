from datetime import datetime
from dateutil.parser import parse
import logging
from lex.responses import get_slot, deny, delegate
from lex.helpers import get_id
from models import user_config


def handler(event):
    webhook = event['currentIntent']['slots'].get('webhook')
    date = event['currentIntent']['slots'].get('date')
    time = event['currentIntent']['slots'].get('time')

    user_id = get_id(event)
    stored_webhook = user_config.get_scheduling_webhook(user_id)
    if not webhook and not stored_webhook:
        return get_slot(event, 'webhook', 'missing_webhook')

    if webhook and webhook != stored_webhook:
        user_config.update_scheduling_webhook(user_id, {
            'last_modified_by': event['userId'],
            'scheduling_webhook': webhook
        })
    
    if not webhook:
        event['currentIntent']['slots']['webhook'] = stored_webhook

    if not date:
        return get_slot(event, 'date', 'missing_date')

    if not time:
        return get_slot(event, 'time', 'missing_time')

    schedule_datetime = parse(str(date) + ' ' + str(time), ignoretz=True)

    if schedule_datetime <= datetime.utcnow():
        return deny(event, 'expired_date_time')

    logging.info('Schedule event on: %s', str(schedule_datetime))

    return delegate(event)
