# aws-local-provisioner

## What is this?

This is a Docker image that helps with creating the basic AWS infrastructure
to use for local development and testing.

All you do is provide the resources in any (or all) of the ways described below!

## Supported resources

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
    image: aws-local-provisioner:latest
    environment:
      AWS_LOCAL_TEMPLATE: |
        version: '2.0'
        resources:
          storage_bucket:
            type: bucket
            name: storage-bucket-eu-west-1
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
