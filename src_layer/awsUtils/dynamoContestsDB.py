import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["CONTESTS_DB"])


def query_contests(groupId):
    response = table.query(
        IndexName="groupContests", KeyConditionExpression=Key("groupId").eq(groupId)
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


def query(id, source):
    response = table.query(
        ExpressionAttributeValues={
            ":xid": id,
            ":xsource": source,
        },
        KeyConditionExpression="id = :xid AND app = :xsource",
    )
    return response["Items"]