from typing import List, Dict, Any, Optional

import botocore.exceptions

import aws.common as common


def _map_attributes(shorthand: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            'AttributeName': attribute_name,
            'AttributeType': attribute_type,
        }
        for attribute_name, attribute_type in shorthand.items()
    ]


def _map_key_schema(shorthand: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            'AttributeName': attribute_name,
            'KeyType': key_type,
        }
        for attribute_name, key_type in shorthand.items()
    ]


def _map_provisioned_throughput(shorthand: Optional[Dict[str, int]]) -> Optional[Dict[str, int]]:
    return None if shorthand is None else common.clear_nones({
        'ReadCapacityUnits': shorthand.get('read'),
        'WriteCapacityUnits': shorthand.get('write'),
    })


def _map_projection(projection_type: Optional[str]):
    return None if projection_type is None else {
        'ProjectionType': projection_type,
    }


def _map_global_secondary_indexes(shorthand_indexes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return None if shorthand_indexes is None else [
        common.clear_nones(dict(
            IndexName=shorthand.get('index_name'),
            Projection=_map_projection(shorthand.get('projection')),
            ProvisionedThroughput=_map_provisioned_throughput(
                shorthand.get('throughput'),
            ),
            KeySchema=_map_key_schema(
                shorthand.get('key_schema')
            ),
        ))
        for shorthand in shorthand_indexes
    ]


def _map_local_secondary_indexes(shorthand_indexes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return None if shorthand_indexes is None else [
        {
            key: value
            for key, value in global_index.items()
            if key != 'ProvisionedThroughput'
        }
        for global_index in _map_global_secondary_indexes(shorthand_indexes)
    ]


def _create_table(table_definition: Dict[str, Any]) -> str:
    client = common.get_client('dynamodb')

    table_name = table_definition.get('name')

    parameters = common.clear_nones(dict(
        TableName=table_name,
        AttributeDefinitions=_map_attributes(
            table_definition.get('attributes')
        ),
        KeySchema=_map_key_schema(
            table_definition.get('key_schema')
        ),
        ProvisionedThroughput=_map_provisioned_throughput(
            table_definition.get('throughput')
        ),
        GlobalSecondaryIndexes=_map_global_secondary_indexes(
            table_definition.get('global_secondary_indexes')
        ),
        LocalSecondaryIndexes=_map_local_secondary_indexes(
            table_definition.get('local_secondary_indexes'),
        )
    ))

    client.create_table(**parameters)

    common.print_resource(
        'Successfully created DynamoDB table',
        meta_dict={'name': table_name}
    )

    return table_name


def _get_global_secondary_updates(shorthand_indexes: List[Dict[str, Any]],
                                  table_name: str) -> [Dict[str, Dict[str, Any]]]:
    client = common.get_client('dynamodb')

    global_secondary_indexes = _map_global_secondary_indexes(shorthand_indexes)

    response = client.describe_table(
        TableName=table_name,
    )

    current_global_secondary_indexes = response['Table'].get(
        'GlobalSecondaryIndexes',
        []
    )

    output = []

    for current_index in current_global_secondary_indexes:
        new_index = common.find(
            global_secondary_indexes,
            lambda index: current_index['IndexName'] == index['IndexName']
        )

        if new_index is None:
            output.append({
                'Delete': {
                    'IndexName': current_index['IndexName']
                }
            })

            continue

        if current_index['ProvisionedThroughput'] != new_index['ProvisionedThroughput']:
            output.append({
                'Update': common.pick_from_dict(
                    new_index,
                    ['IndexName', 'ProvisionedThroughput'],
                )
            })

    for modify_index in global_secondary_indexes:
        existing_index = common.find(
            current_global_secondary_indexes,
            lambda index: modify_index['IndexName'] == index['IndexName']
        )

        if existing_index is None:
            output.append({
                'Create': modify_index,
            })

    return output


def _update_table(table_definition: Dict[str, Any]) -> str:
    client = common.get_client('dynamodb')

    table_name = table_definition.get('name')

    existing_table = client.describe_table(
        TableName=table_name,
    )['Table']

    provisioned_throughput = _map_provisioned_throughput(
        table_definition.get('throughput')
    )

    current_provisioned_throughput = common.pick_from_dict(
        existing_table['ProvisionedThroughput'],
        ['WriteCapacityUnits', 'ReadCapacityUnits']
    )

    if current_provisioned_throughput == provisioned_throughput:
        provisioned_throughput = None

    attribute_definitions = _map_attributes(
        table_definition.get('attributes')
    )

    if common.compare_unordered_lists(attribute_definitions, existing_table['AttributeDefinitions']):
        attribute_definitions = None

    index_updates = _get_global_secondary_updates(
        table_definition.get('global_secondary_indexes'),
        table_name,
    )

    if len(index_updates) == 0:
        index_updates = None

    parameters = common.clear_nones(dict(
        TableName=table_name,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput,
        GlobalSecondaryIndexUpdates=index_updates,
    ))

    if parameters == {'TableName': table_name}:
        common.print_resource(
            'Not updating DynamoDB table, nothing to do',
            meta_dict={'name': table_name}
        )

        return table_name

    client.update_table(**parameters)

    common.print_resource(
        'Successfully updated DynamoDB table',
        meta_dict={'name': table_name}
    )

    return table_name


def create_table(table_definition: Dict[str, Any]) -> str:
    if table_exists(table_definition['name']):
        return _update_table(table_definition)
    else:
        return _create_table(table_definition)


def table_exists(table_name: str) -> bool:
    client = common.get_client('dynamodb')

    try:
        response = client.describe_table(
            TableName=table_name,
        )

        return 'Table' in response
    except botocore.exceptions.ClientError:
        return False
