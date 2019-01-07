# aws-local-provisioner

## What is this?

This is a Docker image that helps with creating the basic AWS infrastructure
to use for local development and testing.

All you do is provide the resources in any (or all) of the ways described below!

## Getting started

### Environment variables

In order for the provisioner to know the URL of the AWS mock, we must provide
these using environment variables. Example: `S3_HOST: http://aws-mock:3000`.

The environment variables should follow the pattern of `<SERVICE_NAME>_HOST` where
`<SERVICE_NAME>` is the service name used in boto3 but all caps.

**Example running s3, sqs, ssm, sns, Kinesis, and DynamoDB**

```yaml
provisioner:
  image: aws-local-provisioner:latest
  environment:
    S3_HOST: http://aws-mock:3000
    SQS_HOST: http://aws-mock:3001
    SSM_HOST: http://aws-mock:3002
    SNS_HOST: http://aws-mock:3003
    KINESIS_HOST: http://aws-mock:3004
    DYNAMODB_HOST: http://aws-mock:3005
    AWS_LOCAL_TEMPLATE_PATH: /aws-local/example-assets/local_template.yaml
  volumes:
    - ./example-assets:/aws-local/example-assets
  depends_on:
    - aws-mock

aws-mock:
  image: localstack/localstack:0.8.6
  environment:
    DEFAULT_REGION: eu-west-1
    SERVICES: s3:3000,sqs:3001,ssm:3002,sns:3003,kinesis:3004,dynamodb:3005
    FORCE_NONINTERACTIVE: 'true'
    HOSTNAME: aws-mock
    HOSTNAME_EXTERNAL: aws-mock
    DEBUG: 0
```

It's also possible to specify a single aws mock, (or mix them).

**Example using single aws mock**

```yaml
moto-provisioner:
  image: aws-local-provisioner:latest
  environment:
    MOCK_AWS_HOST: moto-aws-mock:3000
    AWS_LOCAL_TEMPLATE_PATH: /aws-local/example-assets/local_template.yaml
  volumes:
    - ./example-assets:/aws-local/example-assets
  depends_on:
    - moto-aws-mock

moto-aws-mock:
  image: aws-local-moto-server:latest
  build: moto_host
```

## Supported resources/actions

- S3 buckets
  - S3 file uploads
- SQS queues
  - Subscription for SQS to listen to SNS topics
  - Subscription for SQS to listen for S3 events
- SNS topics
- Kinesis streams
- DynamoDB tables

More are on the way...

## Creating resources

There are three ways to define resources:

  - provide them by a single template environment variable
  - provide them by a mounted template file
  - provide them by separate environment variables

---

### Provisioning through template

Resources can be provided using either the environment variables `AWS_LOCAL_TEMPLATE` or in a (mounted in) template file specified on the environment variable `AWS_LOCAL_TEMPLATE_PATH`.

To use the inline template, resources can be defined like the following in a docker-compose file:

```yaml
version: '2'

services:

  provisioner:
    image: bambora-dkr.jfrog.io/aws-local-provisioner
    environment:
      S3_HOST: aws-mock:3000
      AWS_LOCAL_TEMPLATE: |
        version: '1.0'
        resources:
          storage_bucket:
            type: bucket
            name: storage-bucket-eu-west-1
    depends_on:
      - aws-mock

  aws-mock:
    image: localstack/localstack
    environment:
      DEFAULT_REGION: eu-west-1
      SERVICES: s3:3000
      FORCE_NONINTERACTIVE: 'true'
      HOSTNAME: aws-mock
      HOSTNAME_EXTERNAL: aws-mock
      DEBUG: 0
```

Example template:

```yaml
version: '1.0'

# Dictionary of all resources to provision
resources:

  storage_bucket:
    type: bucket
    name: storage-bucket-eu-west-1
```

Schema definition can be found in [provisioner/schemas/resource_schema_v1.yaml](provisioner/schemas/resource_schema_v1.yaml).

---

### Provisioning through separate environment variables

Schema definition can be found in [provisioner/schemas/resource_schema_environment_variables.yaml](provisioner/schemas/resource_schema_environment_variables.yaml).
