import click
import json
import boto3
import os
from tabulate import tabulate
import awsUtils.dynamoContestsDB as contestsDB
import awsUtils.dynamoSpacesDB as spacesDB


@click.group()
@click.pass_context
async def contest(ctx):
    pass


@contest.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(contest.get_help(ctx))


@contest.command()
@click.pass_context
async def contests_list(ctx):
    result = contestsDB.query_contests(ctx.obj["groupId"])
    if len(result):
        for i in result:
            click.echo(i["name"] + " / " + i["source"])
    else:
        click.echo("Your group doesn't have contests")


@contest.command()
@click.pass_context
async def create_contest():
    pass


@contest.command()
@click.pass_context
@click.argument("contestid")
@click.option("--done", is_flag=True)
async def add_contest(contestid, done):
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


@contest.command()
@click.pass_context
@click.argument("contestid")
async def package_status(ctx, contestid):
    CHROMIUM_CHECK_PACKAGE_STATUS_ARN = os.environ["CHROMIUM_CHECK_PACKAGE_STATUS_ARN"]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "contestId": contestid,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_CHECK_PACKAGE_STATUS_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    allDone = True
    data = []
    for problemIdx, val in body_dict["response"].items():
        data.append([problemIdx, val["curRevision"], val["packageRevision"]])
        if int(val["packageRevision"]) < int(val["curRevision"]):
            allDone = False

    table = (
        "```\n"
        + tabulate(data, headers=["Idx", "curRev", "pkgRev"], tablefmt="pretty")
        + "\n```"
    )
    click.echo(table)

    if allDone:
        click.echo("Package is up to date")
    else:
        click.echo("Packages for some problems are outdated.")
        with click.Context(create_package) as temp_ctx:
            temp_ctx.info_name = "create-package"
            temp_ctx.parent = ctx.parent
            example_usage = create_package.get_usage(temp_ctx).replace("\n", "")
            example_usage = (
                example_usage.replace("[OPTIONS]", "")
                .replace("CONTESTID", contestid)
                .strip()
            )
            click.echo("To update all packages:\n{}".format(example_usage))
            click.echo(
                "If you just used this command, then wait and check the status again."
            )
