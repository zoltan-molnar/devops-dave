from dateutil.parser import parse
from datetime import datetime
from lex.responses import delegate, get_slot, deny


def handler(event):

    date = event['currentIntent']['slots'].get('date')
    time = event['currentIntent']['slots'].get('time')

    if not date:
        return get_slot(event, 'missing_date')

    if not time:
        return get_slot(event, 'missing_time')

    schedule_datetime = parse(str(date) + ' ' + str(time), ignoretz=True)

    if schedule_datetime <= datetime.utcnow():
        return deny(event, 'expired_date_time')

    return delegate(event)
