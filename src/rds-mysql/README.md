# Firehose transformation

## Overview

These functions can perform CRUD operation with AWS RDS.

On cold start, a pymysql connection is created with credentials from SecretsManager.
After that, until the connection gets disconnected, connection will be reused.

## Consideration

- Set proper timeout at least `10s`
- Add Lambda layer `AWS-Parameters-and-Secrets-Lambda-Extension`. It's used to retrieve credentials from SecretsManager
- Add custom Lambda layer for package `pymysql` and `requests`
- Set environment variable `SECRET_NAME`. Also, optionally set others for [extension layer](https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html#ps-integration-lambda-extensions-config)
- Configure VPC to conenct to RDS.

## Permissions

Attach following policies to Lambda role.

- arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
- ```json
  {
    "Effect": "Allow",
    "Action": ["secretsmanager:GetSecretValue"],
    "Resource": "SECRET_ARN"
  }
  ```
