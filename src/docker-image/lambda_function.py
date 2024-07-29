import json
import requests


def handler(event, context):
    print("hello")
    response = requests.get("http://checkip.amazonaws.com")
    print(response.text)
    return {"statusCode": 200, "body": json.dumps({"message": "hello worlds"})}
