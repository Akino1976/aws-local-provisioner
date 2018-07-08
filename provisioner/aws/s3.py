import botocore.exceptions

import aws.common as common


def bucket_exists(client, bucket_name: str) -> bool:
    try:
        client.head_bucket(Bucket=bucket_name)

        return True
    except botocore.exceptions.ClientError:
        return False


def create_bucket(bucket_name: str):
    client = common.get_client('s3')

    if not bucket_exists(client, bucket_name):
        client.create_bucket(Bucket=bucket_name)

        common.print_resource(
            'Bucket created',
            meta_dict={'name': bucket_name}
        )
    else:
        common.print_resource(
            'Bucket already exists',
            meta_dict={'name': bucket_name}
        )

    return bucket_name


def upload_file(s3_file: dict) -> dict:
    client = common.get_client('s3')

    filename = s3_file.get('filename')
    key = s3_file.get('key')
    bucket = s3_file.get('bucket')

    try:
        client.upload_file(
            Filename=filename,
            Bucket=bucket,
            Key=key,
        )

        common.print_resource(
            'Successfully uploaded file to S3',
            meta_dict={'filename': filename, 'bucket': bucket, 'key': key}
        )

        return s3_file
    except botocore.exceptions.ClientError as error:
        common.print_resource(
            'Failed to upload file to S3',
            meta_dict={
                'error': error,
                'filename': filename,
                'bucket': bucket,
                'key': key,
            }
        )
