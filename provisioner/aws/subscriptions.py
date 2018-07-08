
import aws.common as common
import aws.s3 as s3
import aws.ssm as ssm
import aws.sqs as sqs
import aws.kinesis as kinesis
import aws.sns as sns


def subscribe_queue_to_topic(topic_arn: str, queue_url: str):
    client = common.get_client('sns')

    queue_arn = sqs.get_queue_arn(queue_url)

    response = client.list_subscriptions_by_topic(
        TopicArn=topic_arn,
    )

    subscription_exists = any([
        queue_arn == item['Endpoint']
        for item in response['Subscriptions']
    ])

    if subscription_exists:
        common.print_resource(
            'Queue to topic subscription already exists',
            meta_list=[f'topic: {topic_arn}', f'qeue: {queue_arn}']
        )
    else:
        client.subscribe(
            TopicArn=topic_arn,
            Protocol='sqs',
            Endpoint=queue_arn,
        )

        common.print_resource(
            'Added queue subscription on topic',
            meta_list=[f'topic: {topic_arn}', f'qeue: {queue_arn}']
        )


def subscribe_queue_to_bucket(bucket_name: str, queue_url: str, events: list):
    client = common.get_client('s3')

    queue_arn = sqs.get_queue_arn(queue_url)

    client = common.get_client('s3')

    response = client.get_bucket_notification_configuration(
        Bucket=bucket_name
    )

    subscription_exists = any([
        queue_arn == item.get('QueueArn') and item.get('Events') == events
        for item in response.get('QueueConfigurations', [])
    ])

    if subscription_exists:
        common.print_resource(
            'Queue to bucket subscription already exists',
            meta_list=[
                f'bucket: {bucket_name}',
                f'queue: {queue_arn}',
                f'events: {events}',
            ]
        )
    else:
        client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
                'QueueConfigurations': [
                    {
                        'QueueArn': queue_arn,
                        'Events': events
                    }
                ]
            }
        )

        common.print_resource(
            'Created queue to bucket subscription',
            meta_list=[
                f'bucket: {bucket_name}',
                f'queue: {queue_arn}',
                f'events: {events}',
            ]
        )
