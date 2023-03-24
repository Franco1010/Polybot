import click
import json
import boto3
import os
import utils
import uuid
from tabulate import tabulate
import awsUtils.dynamoContestsDB as contestsDB
import awsUtils.dynamoContestRequestsDB as contestRequestDB
import polygon.polygonApi as PolygonApi


@click.group()
@click.pass_context
async def contest(ctx):
    pass


@contest.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(contest.get_help(ctx))


@contest.command(name="list")
@click.pass_context
async def contest_list(ctx):
    result = contestsDB.query_contests(ctx.obj["groupId"])
    if len(result):
        data = []
        for i in result:
            if i["source"] == "polygon":
                data.append([i["name"], i["id"]])
        table = (
            "```\n"
            + tabulate(data, headers=["Name", "Id"], tablefmt="pretty")
            + "\n```"
        )
        click.echo(table)
    else:
        click.echo("Your group doesn't have contests")


@contest.command()
@click.pass_context
@click.argument("name", type=str)
@click.option("--location", type=str, default=None)
@click.option("--date", type=str, default=None)
async def create(ctx, name, location, date):
    """Start new contest development in polygon"""
    CHROMIUM_CREATE_POLYGON_CONTEST = os.environ["CHROMIUM_CREATE_POLYGON_CONTEST"]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "name": name,
            "location": location,
            "date": date,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_CREATE_POLYGON_CONTEST,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    response = body_dict["response"]
    contestId = body_dict["contestId"]
    contestName = body_dict["contestName"]
    click.echo(response)

    if response == "Contest has been created":
        data = [
            ["contestId", contestId],
            ["contestName", contestName],
        ]
        table = "```\n" + tabulate(data, tablefmt="pretty") + "\n```"
        click.echo(table)
        contestsDB.create_item(
            contestId,
            "polygon",
            contestName,
            ctx.obj["groupId"],
        )


@contest.command()
@click.pass_context
@click.argument("contestid")
@click.option("--done", is_flag=True)
async def add(ctx, contestid, done):
    if done:
        res = await add_contest(contestid, ctx.obj["groupId"], ctx)
        click.echo(res)
        return
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine == 2:
        click.echo("Contest is already on the group")
        return
    if mine == 1:
        click.echo("Contest is already added to a group. You cannot added again")
        return
    contest = await PolygonApi.contest(contestid)
    if contest is None:
        click.echo("Polybot doesn't have access to this contest")
        return
    problemId = str(uuid.uuid4())
    contestRequestDB.create_item(
        contestid,
        "polygon",
        ctx.obj["groupId"],
        ctx.obj["callerCtx"]["space"],
        ctx.obj["callerCtx"]["channel"],
        ctx.obj["callerCtx"]["author"],
        problemId,
    )
    click.echo(
        "Add a problem to the contest and change the statement name to: **"
        + problemId
        + "**"
    )
    click.echo("You have 3 minutes")


@contest.command()
@click.argument("contestid")
async def see(ctx, contestid):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("You don't have access to this contest")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return


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


@contest.command()
@click.pass_context
@click.argument("contestid")
async def download_package(ctx, contestid):
    CHROMIUM_DOWNLOAD_PACKAGE_ARN = os.environ["CHROMIUM_DOWNLOAD_PACKAGE_ARN"]
    BUCKET = os.environ["BUCKET"]
    S3WEB = os.environ["S3WEB"]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "contestId": contestid,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_DOWNLOAD_PACKAGE_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    s3Key = body_dict["response"]
    shortUrl = utils.shortPublicS3Url(BUCKET, S3WEB, s3Key)
    click.echo("Latest package created: {}".format(shortUrl))
    with click.Context(package_status) as temp_ctx:
        temp_ctx.info_name = "package-status"
        temp_ctx.parent = ctx.parent
        example_usage = package_status.get_usage(temp_ctx).replace("\n", "")
        example_usage = (
            example_usage.replace("[OPTIONS]", "")
            .replace("CONTESTID", contestid)
            .strip()
        )
        click.echo(
            "If you are not sure about your package being up to date, check package status:\n{}".format(
                example_usage
            )
        )


async def add_contest(contestId, groupId, ctx):
    requests = contestRequestDB.query(groupId, contestId)
    valid = [
        req["auth"]
        for req in requests
        if (
            req["space"] == ctx.obj["callerCtx"]["space"]
            and req["channel"] == ctx.obj["callerCtx"]["channel"]
            and req["author"] == ctx.obj["callerCtx"]["author"]
        )
    ]
    if len(valid) == 0:
        return "No add request pending."
    update_working_copies(contestId)
    contest = await PolygonApi.contest(contestId)
    if contest == None:
        return "Validation failed. Try again"
    for c in contest:
        statements = await PolygonApi.statements(c.id)
        if statements == None:
            continue
        for s in statements:
            click.echo(s.name)
            if s.name in valid:
                contestsDB.create_item(
                    contestId,
                    "polygon",
                    "name",
                    groupId,
                )
                return "Contest added"
    return "Validation failed. Try again"


def is_mine(groupId, contestId):
    res = contestsDB.query(contestId, "polygon")
    if len(res):
        if res[0]["groupId"] == groupId:
            return 2  # mine
        return 1  # owned
    return 0  # not owned


def update_working_copies(contestid):
    CHROMIUM_UPDATE_WORKING_COPIES_ARN = os.environ[
        "CHROMIUM_UPDATE_WORKING_COPIES_ARN"
    ]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "contestId": contestid,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_UPDATE_WORKING_COPIES_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    click.echo(body_dict["response"])
