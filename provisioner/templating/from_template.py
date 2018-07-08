import os
import contextlib

from typing import Dict, List, Any

import yaml

import aws.common as common
import aws.s3 as s3
import aws.ssm as ssm
import aws.sqs as sqs
import aws.kinesis as kinesis
import aws.sns as sns
import aws.dynamodb as dynamodb
import aws.subscriptions as subscriptions

TEMPLATE_VARIABLE_NAME = 'AWS_LOCAL_TEMPLATE'
TEMPLATE_PATH_VARIABLE = 'AWS_LOCAL_TEMPLATE_PATH'


def _get_resource_stubs(template_string: str) -> Dict[str, List[Dict[str, Any]]]:
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

    if not template_string:
        return resource_stubs

    template = yaml.load(template_string)

    for key, value in template.get('resources', {}).items():
        resource_type = value.get('type', '')

        if resource_type.lower() == 'bucket':
            resource_stubs['s3'].append(common.parse_stub(value))
        elif resource_type.lower() == 'queue':
            resource_stubs['sqs'].append(common.parse_stub(value))
        elif resource_type.lower() == 'topic':
            resource_stubs['sns'].append(common.parse_stub(value))
        elif resource_type.lower() == 'ssm_parameter':
            resource_stubs['ssm'].append(common.parse_stub(value))
        elif resource_type.lower() == 'subscription:queue:topic':
            resource_stubs['queue_topic_subscriptions'].append(
                common.parse_stub(value)
            )
        elif resource_type.lower() == 'subscription:queue:bucket':
            resource_stubs['queue_bucket_subscriptions'].append(
                common.parse_stub(value)
            )
        elif resource_type.lower() == 'stream':
            resource_stubs['kinesis'].append(common.parse_stub(value))
        elif resource_type.lower() == 's3_upload':
            resource_stubs['s3_files'].append(common.parse_stub(value))
        elif resource_type.lower() == 'dynamodb_table':
            resource_stubs['dynamodb'].append(common.parse_stub(value))

    return resource_stubs


def get_resource_stubs_from_template_file() -> Dict[str, Dict[str, str]]:
    template_path = os.getenv(TEMPLATE_PATH_VARIABLE)

    template_string = ''

    with contextlib.suppress(TypeError):
        if os.path.exists(template_path):
            with open(template_path) as file:
                template_string = file.read()

    return _get_resource_stubs(template_string)


def get_resource_stubs_from_template_variable() -> Dict[str, Dict[str, str]]:
    template_string = os.getenv(TEMPLATE_VARIABLE_NAME)

    return _get_resource_stubs(template_string)
