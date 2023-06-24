import json

import boto3

client = boto3.client("ec2")


def lambda_handler(event, context):
    try:
        if event["detail"]["eventName"] != "AuthorizeSecurityGroupIngress":
            raise ValueError
        if not event["detail"]["responseElements"]:
            raise ValueError

        rules = event["detail"]["responseElements"]["securityGroupRuleSet"]["items"]
        group_id = rules[0]["groupId"]
        if group_id != "sg-0761b72cc53024020":
            raise ValueError

        rules_to_revoke = []
        for rule in rules:
            protocol = rule["ipProtocol"]
            from_port = rule["fromPort"]
            to_port = rule["toPort"]
            if protocol != "tcp" or from_port != 4272 or to_port != 4272:
                rules_to_revoke.append(rule["securityGroupRuleId"])

        if rules_to_revoke:
            print(rules_to_revoke)
            client.revoke_security_group_ingress(
                GroupId=group_id, SecurityGroupRuleIds=rules_to_revoke
            )

    except (ValueError, KeyError) as e:
        print(e)
    return 200
