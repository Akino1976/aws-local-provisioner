import aws.common as common


def _key_exists(key: str) -> bool:
    client = common.get_client('ssm')

    return len(client.get_parameters(Names=[key]).get('Parameters')) > 0


def provision_key(key: str, value: str):
    client = common.get_client('ssm')

    key_exists = _key_exists(key)

    client.put_parameter(
        Name=key,
        Value=value,
        Type='SecureString',
        Overwrite=True,
    )

    message = 'Updated key in parameter store' if key_exists \
        else 'Created key in parameter store'

    common.print_resource(
        message,
        meta_dict={'key': key, 'value': common.censor(value)}
    )
