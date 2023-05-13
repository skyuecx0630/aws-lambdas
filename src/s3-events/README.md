# Firehose transformation

## Overview

This lambda function will create glue partition on s3 event.

Modify directory or partition settings for your purpose.

## Consideration

- Set environment variable `GLUE_DATABASE_NAME`
- By default, `table_name` variable is inferred from top level directory.
- Be aware of unusual paths like `processing-failed`.

## Permissions

Here's a policy statement for the function.

```json
{
  "Effect": "Allow",
  "Action": ["glue:GetPartition", "glue:CreatePartition", "glue:GetTable"],
  "Resource": "*"
}
```
