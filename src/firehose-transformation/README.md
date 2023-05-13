# Firehose transformation

## Overview

These functions transform data from Kinesis Firehose.

Default structure of codes are from lambda blueprints, but modified for some purposes.

## Consideration

- Set proper timeout, `1min` is recommended.
- To enable `dynamic partitioning`, you must `deaggregate` data first. [Dynamic Partitioning docs](https://docs.aws.amazon.com/firehose/latest/dev/dynamic-partitioning.html)

## Permissions

Here's a policy statement for `cw-logs-transform`.

```json
{
  "Effect": "Allow",
  "Action": ["kinesis:PutRecords", "firehose:PutRecordBatch"],
  "Resource": "*"
}
```
