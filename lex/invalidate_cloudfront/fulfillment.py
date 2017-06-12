from datetime import datetime
from lex.helpers import get_target, get_aws_client, aws_manager_decorator
from lex.responses import fulfill, get_slot


@aws_manager_decorator
def handler(event, aws_config):
    target = get_target(event)

    client = get_aws_client('cloudfront', aws_config)
    client.create_invalidation(
        DistributionId=str(target),
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/*']
            },
            'CallerReference': datetime.utcnow().strftime('%Y%m%d%H%M%S')
        }
    )

    return fulfill(event, 'success')
