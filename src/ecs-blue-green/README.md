# ECS blue green

## Overview

This lambda function is invoked by SNS notifications from CodeDeploy trigger.

Following jobs are performed.

- Get the deployment group
- Get the ECS service which is a target of deployemnt
- Get the replacement task set
- Check a task set stability status until it becomes `STEADY_STATE`

## Consideration

- Set proper timeout, at least `3 min`. It would take some time until ECS service becomes healthy.
- Set environment variables(`RETRY_LIMIT`, `RETRY_INTERVAL`). Or default values(50, 3) will be used.
- Add `DeploymentStart` trigger for a deployment group. And deliver messages using SNS to the function

## Permissions

Here's a policy statement for the function.

```json
{
    "Effect": "Allow",
    "Action": [
        "codedeploy:GetDeploymentGroup",
        "codedeploy:StopDeployment",
        "ecs:DescribeServices",
        "ecs:DescribeTaskSets"
    ],
    "Resource": "*"
}
```
