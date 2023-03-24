import boto3
import os
import time
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["CONTEST_REQUESTS_DB"])


def create_item(id, source, groupId, space, channel, author, auth):
    ttl = int(time.time() + 180)
    table.put_item(
        Item={
            "id": id,
            "source": source,
            "groupId": groupId,
            "space": space,
            "channel": channel,
            "author": author,
            "TimeToLive": ttl,
            "auth": auth,
        }
    )


def query(groupId, contestId):
    response = table.query(
        ExpressionAttributeValues={
            ":xgroupId": groupId,
            ":xid": contestId,
            ":ttl": int(time.time()),
        },
        KeyConditionExpression="#g = :xgroupId AND #i = :xid",
        FilterExpression="#t > :ttl",
        ExpressionAttributeNames={"#g": "groupId", "#i": "id", "#t": "TimeToLive"},
    )
    return response["Items"]
