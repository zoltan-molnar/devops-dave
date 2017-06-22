from dateutil.parser import parse
from lex.responses import fulfill


def handler(event):
    date = event['currentIntent']['slots'].get('date')
    time = event['currentIntent']['slots'].get('time')
    schedule_datetime = parse(str(date) + ' ' + str(time), ignoretz=True)

    event['sessionAttributes']['scheduling_status'] = 'set_in_this_fulfillment'
    event['sessionAttributes']['scheduling_datetime'] = str(schedule_datetime)

    return fulfill(event, 'schedule_set_in_progress')
