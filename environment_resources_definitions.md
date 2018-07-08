
#### S3 buckets

Create an S3 bucket in the local environment.

##### Parameter name format: `*BUCKET_NAME`

##### Parameter value format

_multi-line string with yaml object as content, or the bucket name_

`name` The name of the bucket to create

```yaml
# Bucket name only
STORAGE_BUCKET_NAME: my-storage-bucket-eu-west-1-local

# With YAML object notation
STORAGE_BUCKET_NAME: |
  name: my-storage-bucket-eu-west-1
```

#### S3 file uploads

_Uploads a file from the docker container_

##### Parameter name format: `*S3_UPLOAD`

##### Parameter value format

_multi-line string with yaml object as content_

`filename` The name of the local file (in the docker container). To use non-built in files, simply mount them in into the container

`bucket` Name of the bucket to upload the file to

`key` The key the file should have when uploaded to the bucket

```yaml
CONFIG_S3_UPLOAD: |
  filename: /path/to/mounted/in/file.txt
  bucket: my-storage-bucket-eu-west-1
  key: my/file.txt
```

#### SQS Queues

_Creates an SQS queue by name_

##### Parameter name format: `*QUEUE_NAME`

##### Parameter value format

_multi-line string with yaml object as content, or the queue name_

`name` The name of the queue to create

```yaml
# Queue name only
NOTIFICATIONS_QUEUE_NAME: my-notifications-queue-eu-west-1-local

# With YAML object notation
NOTIFICATIONS_QUEUE_NAME: |
  name: my-notifications-queue-eu-west-1
```

#### Subscription for SQS to listen to SNS topics

_Subscribes an SQS to SNS topic messages_

**Note: Probably won't work everywhere. Should work with [Localstack](https://github.com/localstack/localstack)**

##### Parameter name format: `*QUEUE_TO_TOPIC_SUB`

##### Parameter value format

_multi-line string with yaml object as content_

`queue_name` Name of the queue

`topic_name` Name of the topic

```yaml
CONFIG_QUEUE_TO_TOPIC_SUB: |
  queue_name: my-notifications-queue-eu-west-1-local
  topic_name: my-notifications-topic-eu-west-1-local
```

#### Subscription for SQS to listen for S3 events

_Subscribes an SQS to S3 object events_

**Note: Probably won't work everywhere. Should work with [Localstack](https://github.com/localstack/localstack)**

##### Parameter name format: `*QUEUE_TO_TOPIC_SUB`

##### Parameter value format

_multi-line string with yaml object as content_

`queue_name` Name of the queue

`bucket_name` Name of the bucket

`events` YAML list of [S3 event notification types](https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#notification-how-to-event-types-and-destinations)

```yaml
CONFIG_QUEUE_TO_TOPIC_SUB: |
  queue_name: my-notifications-queue-eu-west-1-local
  bucket_name: my-storage-bucket-eu-west-1-local
  events:
    - s3:ObjectCreated:*
```

#### SNS Topics

_Creates an SNS topic by name_

##### Parameter name format: `*TOPIC_NAME`

##### Parameter value format

_multi-line string with yaml object as content, or the topic name_

`name` The name of the topic to create

```yaml
# Topic name only
NOTIFICATIONS_TOPIC_NAME: my-notifications-topic-eu-west-1-local

# With YAML object notation
NOTIFICATIONS_TOPIC_NAME: |
  name: my-notifications-topic-eu-west-1
```

#### Kinesis streams

_Creates an Kinesis stream by name_

##### Parameter name format: `*STREAM_NAME`

##### Parameter value format

_multi-line string with yaml object as content, or the stream name_

`name` The name of the stream to create

```yaml
# Stream name only
NOTIFICATIONS_STREAM_NAME: my-notifications-stream-eu-west-1-local

# With YAML object notation
NOTIFICATIONS_STREAM_NAME: |
  name: my-notifications-stream-eu-west-1
```

#### DynamoDB tables

_Creates an DynamoDB table by name_

**Note: This one doesn't seem to work very well with moto.**

##### Parameter name format: `*DYNAMODB_TABLE`

##### Parameter value format

_multi-line string with yaml object as content_

`name` The name of the table to create

`attributes` YAML object with the AttributeDefinitions to create.

Keys are mapped to AttributeName and values are mapped AttributeType

`key_schema` YAML object with the KeySchema to create.

Keys are mapped to AttributeName and values are mapped KeyType

`throughput` YAML object containing the ProvisionedThroughput.

Keys are mapped to ReadCapacityUnits and WriteCapacityUnits respective

`global_secondary_indexes` YAML list containing GlobalSecondaryIndexes.

The keys are mapped the same as with top level properties.

`local_secondary_indexes` YAML list containing the LocalSecondaryIndexes.

The keys are mapped the same as with top level properties.

```yaml
MY_DYNAMODB_TABLE: |
  name: some-table
  attributes:
    mainId: S
    createdAt: S
    name: S
  key_schema:
    mainId: HASH
    createdAt: RANGE
  throughput:
    read: 10
    write: 5
  global_secondary_indexes:
    - index_name: SomeGlobalIndex
      projection: ALL
      throughput:
        read: 10
        write: 5
      key_schema:
        name: HASH
        createdAt: RANGE
  local_secondary_indexes:
    - index_name: SomeLocalIndex
      projection: ALL
      key_schema:
        mainId: HASH
        name: RANGE
```


