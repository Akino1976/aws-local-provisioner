import os.path
import enum

from typing import Union

import yaml
import jsonschema

from jsonschema import Draft7Validator

schema_v1_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    './schemas/resource_schema_v1.yaml',
)

schema_environment_variables_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    './schemas/resource_schema_environment_variables.yaml',
)

with open(schema_v1_path) as file:
    template_v1 = file.read()

with open(schema_environment_variables_path) as file:
    template_environment_variables = file.read()

validator_v1 = Draft7Validator(yaml.load(template_v1, Loader=yaml.FullLoader))

environment_parameter_validator = Draft7Validator(
    yaml.load(template_environment_variables, Loader=yaml.FullLoader)
)


class ParameterTypes(enum.Enum):
    BUCKET = 'bucket'
    QUEUE = 'queue'
    TOPIC = 'topic'
    STREAM = 'stream'
    SSM_PARAMETER = 'ssm_parameter'
    S3_UPLOAD = 's3_upload'
    SUBSCRIPTION_QUEUE_BUCKET = 'subscription_queue_bucket'
    SUBSCRIPTION_QUEUE_TOPIC = 'subscription_queue_topic'
    DYNAMODB_TABLE = 'dynamodb_table'


def validate_template(data: dict):
    validation_errors = validator_v1.validate(data)

    if validation_errors is not None:
        raise validation_errors


def validate_environment_variable(value: Union[dict, str],
                                  model_type: enum.Enum):
    validation_errors = environment_parameter_validator.validate({
        model_type.value: value,
    })

    if validation_errors is not None:
        raise validation_errors
