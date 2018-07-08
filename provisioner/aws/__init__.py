
from typing import Dict, List, Any

from . import common
from . import s3
from . import ssm
from . import sqs
from . import kinesis
from . import sns
from . import dynamodb
from . import subscriptions


def create_resources(resource_stubs: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[str, str]]:
    resources = {
        'bucket_names': {},
        'queue_urls': {},
        'topic_arns': {},
        'stream_names': {},
        'tables': {},
        's3_files': {},
    }

    for bucket in resource_stubs['s3']:
        resources['bucket_names'][bucket.get('name')] = s3.create_bucket(
            bucket.get('name')
        )

    for queue in resource_stubs['sqs']:
        resources['queue_urls'][queue.get('name')] = sqs.create_queue(
            queue.get('name')
        )

    for topic in resource_stubs['sns']:
        resources['topic_arns'][topic.get('name')] = sns.create_topic(
            topic.get('name')
        )

    for key_combo in resource_stubs['ssm']:
        ssm.provision_key(key_combo['key'], key_combo['value'])

    for table in resource_stubs['dynamodb']:
        resources['tables'][table['name']] = dynamodb.create_table(table)

    for stream in resource_stubs['kinesis']:
        resources['stream_names'][stream.get('name')] = kinesis.create_stream(
            stream.get('name')
        )

    for subscription in resource_stubs['queue_topic_subscriptions']:
        subscriptions.subscribe_queue_to_topic(
            resources['topic_arns'][subscription['topic_name']],
            resources['queue_urls'][subscription['queue_name']],
        )

    for subscription in resource_stubs['queue_bucket_subscriptions']:
        subscriptions.subscribe_queue_to_bucket(
            resources['bucket_names'][subscription['bucket']],
            resources['queue_urls'][subscription['queue_name']],
            events=subscription['events'],
        )

    for s3_file in resource_stubs['s3_files']:
        resources['s3_files'][s3_file.get('filename')] = s3.upload_file(
            s3_file
        )

    return resources
