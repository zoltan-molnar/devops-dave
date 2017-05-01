from lex.responses import validate_aws_config


def handler(event):
    return validate_aws_config(event)
