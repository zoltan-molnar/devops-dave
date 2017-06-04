import logging
import boto3
from botocore.exceptions import ClientError

from models import user_config, user_alias
from lex.responses import deny, delegate, get_slot


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


def get_aws_config(event):
    config = None

    if not get_missing_aws_config_name(event['sessionAttributes']):
        config = event['sessionAttributes']

    if not config:
        user_id = get_user_id(event['userId'])
        config = user_config.get(user_id).get('config')
        logging.info('User config: %s', str(config))

    if not config:
        team_id = get_team_id(event['userId'])
        config = user_config.get(team_id).get('config')
        logging.info('Team config: %s', str(config))

    event['sessionAttributes'].update(config)

    logging.info('Found config: %s', str(config))
    return config if config else {}


def get_missing_aws_config_name(config):
    required_keys = ['aws_access_key', 'aws_secret_key', 'aws_region']
    for required_key in required_keys:
        if not config or not config.get(required_key):
            return required_key
    return None


def move_slots_into_session(event):
    keys = ['aws_access_key', 'aws_secret_key', 'aws_region']
    for key in keys:
        if event['currentIntent']['slots'].get(key):
            event['sessionAttributes'][key] = event['currentIntent']['slots'][key]


def validate_aws_config(event):

    move_slots_into_session(event)

    logging.info('AWS config in sessionAttributes: %s', event['sessionAttributes'])

    config = get_aws_config(event)

    if get_missing_aws_config_name(config):
        missing_config = get_missing_aws_config_name(event['sessionAttributes'])
        if missing_config:
            event['sessionAttributes']['updateConfig'] = True
            return get_slot(event, missing_config, 'missing_' + missing_config)

    if event['sessionAttributes'].get('updateConfig'):
        event['sessionAttributes']['updateConfig'] = False
        # Insert or update config record
        user_config.update(event['userId'], {
            'last_modified_by': event['userId'],
            'config': {
                'namespace': 'local',
                'aws_access_key': event['sessionAttributes']['aws_access_key'],
                'aws_secret_key': event['sessionAttributes']['aws_secret_key'],
                'aws_region': event['sessionAttributes']['aws_region']
            }
        })

    return delegate(event)


def get_target(event):
    target = str(event['currentIntent']['slots']['target'])

    item_id = get_id(event)
    item = user_alias.get(item_id)

    aliases = item['aliases'] if item and item.get('aliases') else {}

    return aliases[target.lower()] if target.lower() in aliases else target


def get_aws_client(service_name, aws_config):
    return boto3.client(
        service_name,
        aws_access_key_id=aws_config['aws_access_key'],
        aws_secret_access_key=aws_config['aws_secret_key'],
        region_name=aws_config['aws_region'])


def aws_manager_decorator(func):
    def func_wrapper(event):
        aws_config = get_aws_config(event)

        if event['currentIntent']['slots'].get('aws_region'):
            aws_config['aws_region'] = event['currentIntent']['slots']['aws_region']
        try:
            return func(event, aws_config)
        except ClientError as e:
            logging.info('AWS Client error: %s', str(e))
            return deny(event, None, str(e))
        except Exception as e:
            logging.exception(e)
            return deny(event, None, 'Sorry, but an unknown error happened.')
    return func_wrapper
