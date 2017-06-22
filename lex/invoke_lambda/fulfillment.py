from base64 import b64decode
from lex.helpers import get_target, get_aws_client, aws_manager_decorator, can_be_scheduled_decorator
from lex.responses import fulfill, get_slot


@can_be_scheduled_decorator
@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)

    client = get_aws_client('lambda', aws_config)
    lambda_response = client.invoke(
        FunctionName=str(target),
        InvocationType='RequestResponse',
        LogType='Tail',
    )

    response = ''
    log_result = str(lambda_response.get('LogResult', ''))
    function_error = str(lambda_response.get('FunctionError', ''))
    pay_load = lambda_response.get('Payload')

    if log_result:
        response += '*Log:*\n' + b64decode(log_result) + '\n\n'
    if function_error:
        response += '*Function error:*\n' + function_error + '\n\n'
    if pay_load:
        response += '*Response:*\n' + str(pay_load.read()) + '\n\n'

    return fulfill(event, 'success', response)
