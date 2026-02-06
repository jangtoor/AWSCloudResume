import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
ITEM_ID = os.environ.get("ITEM_ID", "visitors")

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        # Atomically increment the counter. If count doesn't exist, start at 0 then add 1.
        resp = table.update_item(
            Key={"Id": ITEM_ID},
            UpdateExpression="SET #c = if_not_exists(#c, :zero) + :inc",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":inc": 1, ":zero": 0},
            ReturnValues="UPDATED_NEW"
        )

        count_val = int(resp["Attributes"]["count"])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"count": count_val})
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
