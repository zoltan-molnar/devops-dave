from random import randint
from utils import file


def get_response(lex_module, response_type):
    global_responses = file.load_json_file('lex/global_responses')
    local_responses = file.load_json_file('lex/' + lex_module + '/responses')

    responses = global_responses.get(response_type, [])
    responses.extend(local_responses.get(response_type, []))

    random_number = randint(0, len(responses) - 1)

    return responses[random_number]


def validate_aws_config(user_id):
    print(user_id)
