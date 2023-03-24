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


def create_item(id, source, name, groupId):
    tableId = str(uuid.uuid4())
    table.put_item(
        Item={
            "id": id,
            "source": source,
            "name": name,
            "groupId": groupId,
            "tableId": tableId,
        }
    )


def query(id, source):
    response = table.query(
        ExpressionAttributeValues={
            ":xid": id,
            ":xsource": source,
        },
        KeyConditionExpression="#i = :xid AND #s = :xsource",
        ExpressionAttributeNames={"#i": "id", "#s": "source"},
    )
    return response["Items"]
