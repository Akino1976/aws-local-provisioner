# Resource definitions

All resources are defined like the following:

```yaml
resource_name:
  type: <resource_type>
  <resource_specific_properties>: <some_value>

# Example
storage_bucket:
  type: bucket
  name: storage-bucket-eu-west-1
```

## Resource definitions

### S3 buckets

`type: bucket`

Create an S3 bucket in the local environment.

`name` The name of the bucket to create

```yaml
storage_bucket_name:
  type: bucket
  type: bucket
  name: my-storage-bucket-eu-west-1
```

### S3 file uploads

`type: s3_upload`

_Uploads a file from the docker container_

`filename` The name of the local file (in the docker container). To use non-built in files, simply mount them in into the container

`bucket` Name of the bucket to upload the file to

`key` The key the file should have when uploaded to the bucket

```yaml
config_s3_upload:
  type: s3_upload
  filename: /path/to/mounted/in/file.txt
  bucket: my-storage-bucket-eu-west-1
  key: my/file.txt
```

### SQS Queues

`type: queue`

_Creates an SQS queue by name_

`name` The name of the queue to create

```yaml
notifications_queue_name:
  type: queue
  name: my-notifications-queue-eu-west-1
```

### Subscription for SQS to listen to SNS topics

`type: subscription:queue:topic`

_Subscribes an SQS to SNS topic messages_

**Note: Probably won't work everywhere. Should work with [Localstack](https://github.com/localstack/localstack)**

`queue_name` Name of the queue

`topic_name` Name of the topic

```yaml
config_queue_to_topic_sub:
  type: subscription
  queue_name: my-notifications-queue-eu-west-1-local
  topic_name: my-notifications-topic-eu-west-1-local
```

### Subscription for SQS to listen for S3 events

`type: subscription:queue:bucket`

_Subscribes an SQS to S3 object events_

**Note: Probably won't work everywhere. Should work with [Localstack](https://github.com/localstack/localstack)**

`queue_name` Name of the queue

`bucket_name` Name of the bucket

`events` YAML list of [S3 event notification types](https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#notification-how-to-event-types-and-destinations)

```yaml
config_queue_to_bucket_sub:
  type: subscription
  queue_name: my-notifications-queue-eu-west-1-local
  bucket_name: my-storage-bucket-eu-west-1-local
  events:
    - s3:ObjectCreated:*
```

### SNS Topics

`type: topic`

_Creates an SNS topic by name_

`name` The name of the topic to create

```yaml
notifications_topic_name:
  type: topic
  name: my-notifications-topic-eu-west-1
```

### Kinesis streams

`type: stream`

_Creates an Kinesis stream by name_

`name` The name of the stream to create

```yaml
notifications_stream_name:
  type: stream
  name: my-notifications-stream-eu-west-1
```

### DynamoDB tables

`type: dynamodb_table`

_Creates an DynamoDB table by name_

**Note: This one doesn't seem to work very well with moto.**

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
my_dynamodb_table:
  type: dynamodb_table
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


