import base64
import json


def lambda_handler(event, context):
    output = []

    for record in event["records"]:
        payload = base64.b64decode(record["data"]).decode("utf-8")

        message = json.loads(payload)
        try:
            booking_record = {
                "Id": message["data"]["id"],
                "Hotelid": message["data"]["hotelID"],
                "customerid": message["data"]["customerID"],
            }

            data = json.dumps(booking_record) + "\n"

            print(data)
            output_record = {
                "recordId": record["recordId"],
                "result": "Ok",
                "data": base64.b64encode(data.encode("utf-8")).decode("utf-8"),
            }
        except KeyError:
            output_record = {
                "recordId": record["recordId"],
                "result": "Dropped",
                "data": base64.b64encode(payload.encode("utf-8")).decode("utf-8"),
            }

        output.append(output_record)

    print("Successfully processed {} records.".format(len(event["records"])))

    return {"records": output}
