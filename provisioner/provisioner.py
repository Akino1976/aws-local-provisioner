from functools import reduce

import aws
import aws
import templating.from_env_vars as from_env_vars
import templating.from_template as from_template


def provision_resources():
    aws.common.wait_for_connection(0)

    resource_stub_list = [
        from_template.get_resource_stubs_from_template_file(),
        from_template.get_resource_stubs_from_template_variable(),
        from_env_vars.get_resource_stubs(),
    ]

    resource_stubs = {}

    for stub in resource_stub_list:
        for key, stub_value in stub.items():
            resource_stubs[key] = reduce(
                lambda base, value: (
                    [*base, value] if value not in base else base
                ),
                resource_stubs.get(key, []) + stub_value,
                []
            )

    print('Creating resources:')
    print('')

    aws.create_resources(resource_stubs)

    print('')
    print('Resources provisioned!')


if __name__ == '__main__':
    provision_resources()
