import handler
import logging


def lambda_handler(event, context):
    logging.info('custom handler yeah')
    return handler.lambda_handler(event, context)
