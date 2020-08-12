
import os
import time

from typing import Callable, Any, List, Dict, Union, Optional

import boto3
import botocore.config
import yaml

AWS_REGION = os.getenv('AWS_REGION', 'eu-west-1')


def _get_proxy(service_name: str) -> Optional[str]:
    service_proxy = os.getenv(f'{service_name.upper()}_HOST')

    if service_proxy is not None:
        return service_proxy

    return os.getenv('MOCK_AWS_HOST')


def get_client(service_name: str):
    proxy = _get_proxy(service_name)

    params = dict(
        service_name=service_name,
        region_name=AWS_REGION,
        config=botocore.config.Config(
            connect_timeout=1,
            read_timeout=1,
            retries={'max_attempts': 5}
        )
    )

    if proxy is not None:
        params['use_ssl'] = proxy.startswith('https://')
        params['config'].proxies = {'http': proxy}

    return boto3.client(**params)


def wait_for_connection(resource_types=List[str],
                        initial_timeout: Optional[int]=5):
    attempts = 0

    checks = []

    if 's3' in resource_types:
        s3_client = get_client('s3')
        checks.append(lambda: s3_client.list_buckets())
    if 'sqs' in resource_types:
        sqs_client = get_client('sqs')
        checks.append(lambda: sqs_client.list_queues())
    if 'sns' in resource_types:
        sns_client = get_client('sns')
        checks.append(lambda: sns_client.list_topics())
    if 'dynamodb' in resource_types:
        dynamodb_client = get_client('dynamodb')
        checks.append(lambda: dynamodb_client.list_tables())
    if 'kinesis' in resource_types:
        kinesis_client = get_client('kinesis')
        checks.append(lambda: kinesis_client.list_streams())

    print('Attempting to connect to aws-mock')

    time.sleep(initial_timeout)

    while attempts < 30:
        try:
            for check in checks:
                check()

            print('Connected to aws-mock!')
            print('')
            break
        except Exception as error:
            print(f'Retrying to connect to aws-mock: {error}')

            attempts += 1
            time.sleep(1)


def clear_nones(dct: dict) -> dict:
    return {
        key: value
        for key, value in dct.items()
        if value is not None
    }


def find(coll: List[Any], predicate: Callable[[Any], bool]) -> Any:
    if coll is not None:
        for item in coll:
            if predicate(item):
                return item

    return None


def pick_from_dict(dct: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    return {
        key: dct.get(key)
        for key in keys
    }


def compare_unordered_lists(list1: list, list2: list) -> bool:
    if len(list1) != len(list2):
        return False

    return all([
        item in list2
        for item in list1
    ])


def _get_stub_with_name(value: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    parsed_value = yaml.load(value, Loader=yaml.FullLoader) \
        if isinstance(value, str) \
        else value

    if isinstance(parsed_value, str):
        return {'name': parsed_value}

    return parsed_value


def parse_stub(value: str) -> Dict[str, Any]:
    output = _get_stub_with_name(value)

    return {
        key: value
        for key, value in output.items()
        if key != 'type'
    }


def print_resource(message: str,
                   meta_list: Optional[List[str]]=[],
                   meta_dict: Optional[Dict[str, str]]={}):
    # TODO: Just use YAML to format the meta properties
    print('> ' + '\n'.join([
        message,
        *[f'    - {item}' for item in meta_list],
        *[f'    {key}: {value}' for key, value in meta_dict.items()],
    ]))


def censor(value: str, max_visible: Optional[int]=4) -> str:
    visible_chars = len(value) // 4

    if visible_chars > max_visible:
        visible_chars = max_visible

    return ''.join([
        value[:visible_chars],
        *['x' for char in value[visible_chars:]],
    ])
