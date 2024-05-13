import os
import sys
import logging
import pymysql
import json
import requests


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# rds settings

CONNECTION = None


def get_connection():
    global CONNECTION
    if CONNECTION:
        return CONNECTION

    SECRET_NAME = os.environ.get("SECRET_NAME")
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN")}
    secrets_extension_endpoint = (
        f"http://localhost:2773/secretsmanager/get?secretId={SECRET_NAME}"
    )

    r = requests.get(secrets_extension_endpoint, headers=headers)
    secret = json.loads(
        json.loads(r.text)["SecretString"]
    )  # load the Secrets Manager response into a Python dictionary, access the secret

    rds_host = secret["host"]
    user_name = secret["username"]
    password = secret["password"]
    db_name = secret["database"]

    # create the database connection outside of the handler to allow connections to be
    # re-used by subsequent function invocations.
    try:
        CONNECTION = pymysql.connect(
            host=rds_host,
            user=user_name,
            passwd=password,
            db=db_name,
            connect_timeout=5,
        )
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    return CONNECTION


def lambda_handler(event, context):
    conn = get_connection()

    name = event["name"]
    category = event["category"]

    sql_product_insert = "insert into product (name, category) values(%s, %s)"
    with conn.cursor() as cur:
        cur.execute(sql_product_insert, (name, category))
        conn.commit()
        id = cur.lastrowid
    conn.commit()

    return {"message": f"Row inserted. id is {id}"}
