from lex.helpers import get_id
from lex.responses import fulfill, confirm
from models import user_alias


def handler(event):
    alias = str(event['currentIntent']['slots']['alias']).lower()
    target = str(event['currentIntent']['slots']['target'])

    item_id = get_id(event)
    item = user_alias.get(item_id)

    aliases = item['aliases'] if item and item.get('aliases') else {}

    if item and alias in aliases:
        response = confirm(event)
        if response:
            return response

    aliases[alias] = target
    # Insert or update config record
    user_alias.update(item_id, {
        'last_modified_by': event['userId'],
        'aliases': aliases
    })

    return fulfill(event, 'success')
