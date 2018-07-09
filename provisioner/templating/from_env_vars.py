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
import validator


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
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.BUCKET
            )

            resource_stubs['s3'].append(common.parse_stub(value))
        elif key.endswith('QUEUE_NAME'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.QUEUE
            )

            resource_stubs['sqs'].append(common.parse_stub(value))
        elif key.endswith('TOPIC_NAME'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.TOPIC
            )

            resource_stubs['sns'].append(common.parse_stub(value))
        elif key.endswith('SSM_PARAMETER'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.SSM_PARAMETER
            )

            resource_stubs['ssm'].append(common.parse_stub(value))
        elif key.endswith('QUEUE_TO_TOPIC_SUB'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.SUBSCRIPTION_QUEUE_TOPIC
            )

            resource_stubs['queue_topic_subscriptions'].append(
                common.parse_stub(value)
            )
        elif key.endswith('QUEUE_TO_BUCKET_SUB'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.SUBSCRIPTION_QUEUE_BUCKET
            )

            resource_stubs['queue_bucket_subscriptions'].append(
                common.parse_stub(value)
            )
        elif key.endswith('STREAM_NAME'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.STREAM
            )

            resource_stubs['kinesis'].append(common.parse_stub(value))
        elif key.endswith('S3_UPLOAD'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.S3_UPLOAD
            )

            resource_stubs['s3_files'].append(common.parse_stub(value))
        elif key.endswith('DYNAMODB_TABLE'):
            validator.validate_environment_variable(
                yaml.load(value),
                validator.ParameterTypes.DYNAMODB_TABLE
            )

            resource_stubs['dynamodb'].append(common.parse_stub(value))

    return resource_stubs
