import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["SPACES_DB"])


def query(id, app):
    response = table.query(
        ExpressionAttributeValues={
            ":xid": id,
            ":xapp": app,
        },
        KeyConditionExpression="id = :xid AND app = :xapp",
    )
    return response["Items"]
