from datetime import datetime, timedelta
import base64
import json

TIMEZONE_OFFSET_HOUR = 9
TIMEZONE_OFFSET_MINUTE = 0


def lambda_handler(event, context):
    firehose_stream = event["deliveryStreamArn"]
    records = event["records"]
    print(f"Received event from {firehose_stream}. Total {len(records)} records.")

    # return {'records': output_records}
    output_records = []

    for record in records:
        try:
            data = json.loads(base64.b64decode(record["data"]))

            record_datetime = datetime.strptime(
                data["timestamp"], "%Y-%m-%dT%H:%M:%S"
            ) + timedelta(hours=TIMEZONE_OFFSET_HOUR, minutes=TIMEZONE_OFFSET_MINUTE)
            data["timestamp"] = record_datetime.isoformat(timespec="seconds")
        except KeyError:
            output_records.append({"recordId": record["recordId"], "result": "Dropped"})

        partitionKeys = {
            "type": data["type"],
            "deviceId": data["device_id"],
            "year": record_datetime.strftime("%Y"),
            "month": record_datetime.strftime("%m"),
            "day": record_datetime.strftime("%d"),
            "hour": record_datetime.strftime("%H"),
        }

        output_records.append(
            {
                "recordId": record["recordId"],
                "data": base64.b64encode(json.dumps(data).encode()),
                "result": "Ok",
                "metadata": {"partitionKeys": partitionKeys},
            }
        )

    return {"records": output_records}
