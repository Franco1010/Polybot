import boto3
import os
import uuid

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


def create_item(id, app, name):
    groupId = str(uuid.uuid4())
    tableId = str(uuid.uuid4())
    table.put_item(
        Item={
            "id": id,
            "app": app,
            "name": name,
            "groupId": groupId,
            "tableId": tableId,
        }
    )
    return groupId
