import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key
from datetime import date

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["REQUESTS_DB"])


def query(groupId):
    response = table.query(KeyConditionExpression=Key("groupId").eq(groupId))
    return response["Items"]


def query_request(groupId, requestId):
    response = table.query(
        ExpressionAttributeValues={
            ":xid": groupId,
            ":xreqId": requestId,
        },
        KeyConditionExpression="#i = :xid AND #s = :xreqId",
        ExpressionAttributeNames={"#i": "groupId", "#s": "requestId"},
    )
    return response["Items"]


def create_item(groupId, server, space, name):
    requestId = str(uuid.uuid4())
    table.put_item(
        Item={
            "groupId": groupId,
            "requestId": requestId,
            "server": server,
            "space": space,
            "name": name,
            "date": str(date.today()),
            "status": "pending",
        }
    )
    return requestId


def update_status(groupId, requestId, status):
    table.update_item(
        Key={
            "groupId": groupId,
            "requestId": requestId,
        },
        UpdateExpression="set #s = :s",
        ExpressionAttributeValues={
            ":s": status,
        },
        ExpressionAttributeNames={
            "#s": "status",
        },
    )