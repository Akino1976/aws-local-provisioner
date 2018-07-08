import os

from typing import Dict, List, Any, Union

import yaml

import aws.common as common
import aws.s3 as s3
import aws.ssm as ssm
import aws.sqs as sqs
import aws.kinesis as kinesis
import aws.sns as sns
import aws.dynamodb as dynamodb
import aws.subscriptions as subscriptions


def get_resource_stubs() -> Dict[str, List[Any]]:
    resource_stubs = {
        's3': [],
        'sqs': [],
        'sns': [],
        'ssm': [],
        'kinesis': [],
        'queue_topic_subscriptions': [],
        'queue_bucket_subscriptions': [],
        's3_files': [],
        'dynamodb': [],
    }

    for key in os.environ.keys():
        key = str(key)
        value = os.getenv(key)

        if key.endswith('BUCKET_NAME'):
            resource_stubs['s3'].append(common.parse_stub(value))
        elif key.endswith('QUEUE_NAME'):
            resource_stubs['sqs'].append(common.parse_stub(value))
        elif key.endswith('TOPIC_NAME'):
            resource_stubs['sns'].append(common.parse_stub(value))
        elif key.endswith('KEY_COMBO'):
            resource_stubs['ssm'].append(common.parse_stub(value))
        elif key.endswith('QUEUE_TO_TOPIC_SUB'):
            resource_stubs['queue_topic_subscriptions'].append(
                common.parse_stub(value)
            )
        elif key.endswith('QUEUE_TO_BUCKET_SUB'):
            resource_stubs['queue_bucket_subscriptions'].append(
                common.parse_stub(value)
            )
        elif key.endswith('STREAM_NAME'):
            resource_stubs['kinesis'].append(common.parse_stub(value))
        elif key.endswith('S3_UPLOAD'):
            resource_stubs['s3_files'].append(common.parse_stub(value))
        elif key.endswith('DYNAMODB_TABLE'):
            resource_stubs['dynamodb'].append(common.parse_stub(value))

    return resource_stubs
