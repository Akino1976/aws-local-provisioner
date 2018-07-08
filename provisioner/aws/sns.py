import aws.common as common


def create_topic(topic_name: str) -> str:
    client = common.get_client('sns')

    response = client.create_topic(Name=topic_name)

    topic_arn = response['TopicArn']
    common.print_resource(
        'Created SNS topic',
        meta_dict={'name': topic_name, 'topic_arn': topic_arn}
    )

    return topic_arn
