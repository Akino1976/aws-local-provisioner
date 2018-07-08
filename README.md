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
# Optional versioning parameter. Not used right now, but might be useful to enable legacy formats.
version: '1.0'

# Dictionary of all resources to provision
resources:

  storage_bucket:
    type: bucket
    name: storage-bucket-eu-west-1
```

####  `[version]` _Optional_

Specifies what template parser version to use. Currently doesn't matter.

```yaml
version: '1.0'
```

#### `resources` **Required**

The resources to create/update. Each key should contain a resource to create.

```yaml
resources:

  storage_bucket:
    type: bucket
    name: storage-bucket-eu-west-1
```

Resource definitions can be found in the file `resource_definitions.md`

---

### Provisioning through separate environment variables

Resources can be provided using environment variables, described here: `environment_resources_definitions.md`
