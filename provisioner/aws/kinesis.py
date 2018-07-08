import botocore.exceptions

import aws.common as common


def create_stream(stream_name: str, shard_count: int=1) -> str:
    client = common.get_client('kinesis')

    try:
        response = client.describe_stream(
            StreamName=stream_name
        )

        stream_exists = 'StreamDescription' in response
    except botocore.exceptions.ClientError:
        stream_exists = False

    if not stream_exists:
        client.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count,
        )
        common.print_resource(
            'Kinesis stream created',
            meta_dict={'name': stream_name}
        )
    else:
        common.print_resource(
            'Kinesis stream already exists',
            meta_dict={'name': stream_name}
        )

    return stream_name
