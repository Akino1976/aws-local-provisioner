import botocore.exceptions

import aws.common as common


def create_queue(queue_name: str) -> str:
    client = common.get_client('sqs')

    try:
        response = client.get_queue_url(QueueName=queue_name)

        queue_url = response['QueueUrl']
        common.print_resource(
            'Queue already exists, not creating it',
            meta_dict={'queue_name': queue_name, 'queue_url': queue_url}
        )

        return queue_url
    except botocore.exceptions.ClientError:
        response = client.create_queue(QueueName=queue_name)

        queue_url = response['QueueUrl']
        common.print_resource(
            'Created queue',
            meta_dict={'queue_name': queue_name, 'queue_url': queue_url}
        )

        return queue_url


def get_queue_arn(queue_url: str) -> str:
    client = common.get_client('sqs')

    response = client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['QueueArn']
    )

    return response['Attributes']['QueueArn']
