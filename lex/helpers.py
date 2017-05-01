from models import user_config


def get_namespace(namespace):
    variants = {
        'global': ['global', 'team'],
        'local': ['local', 'my']
    }

    for key, options in variants.iteritems():
        if namespace and namespace in options:
            return key

    return ''


def get_team_id(lex_user_id):
    # This one works with Slack, no idea about the others
    return ':'.join(str(lex_user_id).split(':')[:2])


def get_user_id(lex_user_id):
    return str(lex_user_id)


def get_id(event):
    namespace = get_namespace(event['currentIntent']['slots'].get('namespace'))

    if namespace == 'global':
        return get_team_id(event['userId'])

    return get_user_id(event['userId'])


def get_aws_config(id_from_app):
    user_id = get_user_id(id_from_app)
    config = user_config.get(user_id).get('config')
    if not config:
        team_id = get_team_id(id_from_app)
        config = user_config.get(team_id).get('config')
    return config
