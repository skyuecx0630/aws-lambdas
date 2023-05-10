from time import sleep
import os
import json

import boto3

codedeploy = boto3.client("codedeploy")
ecs = boto3.client("ecs")
RETRY_LIMIT = int(os.getenv("RETRY_LIMIT", 50))
RETRY_INTERVAL = int(os.getenv("RETRY_INTERVAL", 3))


def retry(times=RETRY_LIMIT, interval=RETRY_INTERVAL):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry = 0
            result = func(*args, **kwargs)

            while result is None and retry < times:
                retry += 1
                sleep(interval)
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def get_valid_event_message(event):
    for record in event["Records"]:
        try:
            message = json.loads(record["Sns"]["Message"])
            if message["eventTriggerName"] == "deployment-start":
                return message
        except KeyError:
            continue
    return


def get_target_service(message):
    application_name = message["applicationName"]
    deployment_group_name = message["deploymentGroupName"]

    deployment_target = codedeploy.get_deployment_group(
        applicationName=application_name, deploymentGroupName=deployment_group_name
    )["deploymentGroupInfo"]["ecsServices"][0]

    return deployment_target


def get_service(cluster_name, service_name):
    services = ecs.describe_services(cluster=cluster_name, services=[service_name])[
        "services"
    ]

    return services[0] if services else None


def get_task_set(cluster_name, service_name, task_set_id):
    task_sets = ecs.describe_task_sets(
        cluster=cluster_name, service=service_name, taskSets=[task_set_id]
    )["taskSets"]
    return task_sets[0] if task_sets else None


@retry(times=5, interval=2)
def get_replacement_task_set(cluster_name, service_name):
    service = get_service(cluster_name, service_name)
    if service is None:
        return

    replacement_task_sets = list(
        filter(lambda x: x["status"] == "ACTIVE", service["taskSets"])
    )

    return replacement_task_sets[0] if replacement_task_sets else None


@retry(times=50, interval=3)
def wait_task_set_stable(cluster_name, service_name, task_set_id):
    task_set = get_task_set(cluster_name, service_name, task_set_id)

    if task_set and task_set["stabilityStatus"] == "STEADY_STATE":
        return task_set
    return None


def lambda_handler(event, context):
    message = get_valid_event_message(event)
    if message is None:
        print("Invalid events:", event)
        return

    deployment_id = message["deploymentId"]

    print(f"Deployment: {deployment_id}")

    target_service = get_target_service(message)
    cluster_name = target_service["clusterName"]
    service_name = target_service["serviceName"]

    task_set = get_replacement_task_set(cluster_name, service_name)
    if task_set is None:
        print("Replacement task set not found")
        print(target_service)
        return

    print(f"Task set: {task_set['id']}")

    stable = wait_task_set_stable(cluster_name, service_name, task_set["id"])

    if not stable:
        print(f"{deployment_id} is considered unhealthy. Stopping deployment")
        response = codedeploy.stop_deployment(
            deploymentId=deployment_id, autoRollbackEnabled=True
        )
        print(response)
        return
    print(f"{deployment_id} is considered healthy.")
    return
