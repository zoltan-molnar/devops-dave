import logging
from dateutil.parser import parse
from lex.responses import fulfill


def handler(event):
    date = event['currentIntent']['slots'].get('date')
    time = event['currentIntent']['slots'].get('time')

    schedule_datetime = parse(str(date) + ' ' + str(time), ignoretz=True)

    logging.info('Schedule event on: %s', str(schedule_datetime))

    return fulfill(event, 'schedule_set')
