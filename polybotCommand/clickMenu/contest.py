import sys
import click
import json
import boto3
import os


@click.group()
async def contest():
    pass


@contest.command()
async def contests_list():
    pass


@contest.command()
async def create_contest():
    pass


@contest.command()
@click.argument("contestid")
async def add_contest(contestId):
    pass


@contest.command()
@click.argument("contestid")
async def see_contest(contestid):
    pass


@contest.command()
@click.argument("contestid")
async def create_package(contestid):
    CHROMIUM_CREATE_POLYGON_PACKAGE_ARN = os.environ[
        "CHROMIUM_CREATE_POLYGON_PACKAGE_ARN"
    ]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "contestId": contestid,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_CREATE_POLYGON_PACKAGE_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    click.echo(body_dict["response"])
