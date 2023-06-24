# EventBridge

## Overview

This function will receive cloudtrail event, and checks security group rule is allowed.

## Consideration

- CloudTrail must be enabled to capture `AuthorizeSecurityGroupIngress` evnet
- Configure EventBridge rule which delivers `AuthorizeSecurityGroupIngress` to this function.

## Permissions

Here's a policy statement for the function.

```json
{
  "Effect": "Allow",
  "Action": ["ec2:RevokeSecurityGroupIngress"],
  "Resource": "*"
}
```
