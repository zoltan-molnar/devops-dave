from copy import copy
import logging
import boto3
from botocore.exceptions import ClientError

from utils.slack import send_message_via_webhook
from models import user_config, user_alias, scheduled_action
from lex.responses import deny, delegate, get_slot, fulfill


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

    if not config:
        team_id = get_team_id(event['userId'])
        config = user_config.get(team_id).get('config')

    config = config if config else {}

    event['sessionAttributes'].update(config)

    return config


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

    return False


def get_target(event):
    target = str(event['currentIntent']['slots']['target'] if event['currentIntent']['slots']['target'] else '')

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


def get_aws_resource(resource_name, aws_config):
    return boto3.resource(
        resource_name,
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


def aws_validator_decorator(func):
    def func_wrapper(event):
        invalid = validate_aws_config(event)
        if invalid:
            return invalid
        return func(event)
    return func_wrapper


def can_be_scheduled_decorator(func):
    def func_wrapper(event):
        if event['sessionAttributes'] and event['sessionAttributes'].get('scheduling_status'):
            if event['sessionAttributes']['scheduling_status'] == 'scheduling':
                return __schedule(event)
        try:
            if event['sessionAttributes'] and event['sessionAttributes'].get('scheduling_status'):
                if event['sessionAttributes']['scheduling_status'] == 'processing':
                    response = func(event)
                    send_response_to_slack(event, response)
                    return response
            return func(event)
        except Exception as e:
            logging.exception(e)
            return deny(event, None, 'Sorry, but an unknown error happened.')
    return func_wrapper


def send_response_to_slack(event, response):
    user_id = get_id(event)
    webhook = user_config.get_scheduling_webhook(user_id)

    content = response['dialogAction']['message']['content']

    return send_message_via_webhook(webhook, {'text': content})


def __schedule(event):
    event_copy = copy(event)
    event_copy['sessionAttributes'] = {}

    scheduled_datetime = event['sessionAttributes']['scheduling_datetime']

    scheduled_action.add({
        'added_by': get_id(event_copy),
        'event': event_copy,
        'scheduled_datetime': scheduled_datetime,
        'execution_status': 'not_started'
    })

    return fulfill(event, 'schedule_set')
