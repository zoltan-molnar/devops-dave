from lex.responses import fulfill


def handler(event):
    return fulfill(event, None, '42')
