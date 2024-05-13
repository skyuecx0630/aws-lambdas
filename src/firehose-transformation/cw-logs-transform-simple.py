import json
import gzip
import base64

DECOMPRESSED_CW_LOGS = False
EXTRACTED_MESSAGE_FILEDS = False


def transform_data(data):
    # Implement transfromation logic here
    return data


def lambda_handler(event, context):
    print(json.dumps(event, indent=2))

    output_records = []

    for record in event["records"]:
        data = record["data"]

        if not DECOMPRESSED_CW_LOGS:
            data = json.loads(gzip.decompress(base64.b64decode(record["data"])))
        if not EXTRACTED_MESSAGE_FILEDS:
            data = data["message"]

        transformed_data = transform_data(data)

        output_records.append(
            {
                "recordId": record["recordId"],
                "data": base64.b64encode(json.dumps(transformed_data).encode()),
                "result": "Ok",
            }
        )

    return {"records": output_records}
