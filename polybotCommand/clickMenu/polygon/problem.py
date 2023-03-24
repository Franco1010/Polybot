import sys
import click
import awsUtils.dynamoContestsDB as contestsDB
import polygon.polygonApi as PolygonApi
from tabulate import tabulate
import utils
import os
import json
import boto3


@click.group()
@click.pass_context
async def problem(ctx):
    pass


@problem.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(problem.get_help(ctx))


@problem.command()
@click.argument("contestid")
@click.pass_context
@click.argument("problemname")
async def create(contestid, problemname):
    res = create_problem(contestid, problemname)
    click.echo(res["response"])
    data = [["problemName", res["problemName"]], ["problemIdx", res["problemIdx"]]]
    table = "```\n" + tabulate(data, tablefmt="pretty") + "\n```"
    click.echo(table)
    res = commit_changes(contestid, res["problemIdx"])
    click.echo(res)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.pass_context
async def info(ctx, contestid, problemid):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    data = []
    for c in contest:
        if c.letter == problemid:
            data.append(["name", c.name])
            data.append(["owner", c.owner])
            info = await PolygonApi.info(c.id)
            if info != None:
                data.append(["timeLimit", str(info.timeLimit) + "ms"])
                data.append(["memoryLimit", str(info.memoryLimit) + "mb"])
                data.append(["interactive", info.interactive])
            table = "```\n" + tabulate(data, tablefmt="pretty") + "\n```"
            click.echo(table)
            break
    click.echo("Problem is not available")


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.pass_context
async def download_package(ctx, contestid, problemid):
    BUCKET = os.environ["BUCKET"]
    S3WEB = os.environ["S3WEB"]
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    packages = await PolygonApi.packages(p.id)
    if packages == None:
        click.echo("Problem has no packages")
        return
    packages = [p for p in packages if p.state == "READY"]
    if packages == None:
        click.echo("Problem has no ready packages")
        return
    pack = packages[-1]
    s3Key = PolygonApi.download_package(p.id, pack.id)
    shortUrl = utils.shortPublicS3Url(BUCKET, S3WEB, s3Key)
    click.echo("Check latest package created: {}".format(shortUrl))


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.argument("solution")
@click.argument("tag")
@click.pass_context
async def add_solution(ctx, contestid, problemid, solution, tag):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    res = await PolygonApi.save_solution(p.id, solution, tag)
    click.echo(res)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.argument("lang")
@click.argument("name")
@click.argument("legend")
@click.argument("input")
@click.argument("output")
@click.pass_context
async def add_statement(ctx, contestid, problemid, lang, name, legend, input, output):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    res = await PolygonApi.save_statement(p.id, lang, name, legend, input, output)
    click.echo(res)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.argument("test")
@click.pass_context
async def add_test(ctx, contestid, problemid, test):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    res = await PolygonApi.tests(p.id, "tests")
    if res == None:
        newtest = await PolygonApi.save_test(p.id, "tests", 1, test)
        click.echo("1")
        return
    newtest = await PolygonApi.save_test(p.id, "test", len(res) + 1, test)
    click.echo(len(res) + 1)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.pass_context
async def solutions(ctx, contestid, problemid):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    res = await PolygonApi.solutions(p.id)
    if res == None:
        click.echo("Problem doesn't have solutions")
        return
    data = [[s.name, s.sourceType, s.tag] for s in res]
    table = (
        "```\n"
        + tabulate(data, headers=["Name", "Source", "Tag"], tablefmt="pretty")
        + "\n```"
    )
    click.echo(table)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.pass_context
async def statements(ctx, contestid, problemid):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    res = await PolygonApi.statements(p.id)
    if res == None:
        click.echo("Problem doesn't have statements")
        return
    data = [[s.lang, s.name] for s in res]
    table = (
        "```\n"
        + tabulate(data, headers=["Language", "Name"], tablefmt="pretty")
        + "\n```"
    )
    click.echo(table)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.argument("checker")
@click.pass_context
async def set_checker(ctx, contestid, problemid, checker):
    mine = is_mine(ctx.obj["groupId"], contestid)
    if mine != 2:
        click.echo("Polybot doesn't have access to this problem")
        return
    contest = await PolygonApi.contest(contestid)
    if contest == None:
        click.echo("Contest is missing write access.")
        return
    p = None
    for c in contest:
        if c.letter == problemid:
            p = c
            break
    if p == None:
        click.echo("Problem is not in contest.")
        return
    res = await PolygonApi.set_checker(p.id, checker)
    click.echo(res)


def is_mine(groupId, contestId):
    res = contestsDB.query(contestId, "polygon")
    if len(res):
        if res[0]["groupId"] == groupId:
            return 2  # mine
        return 1  # owned
    return 0  # not owned


def create_problem(contestid, problemname):
    CHROMIUM_CREATE_POLYGON_PROBLEM_ARN = os.environ[
        "CHROMIUM_CREATE_POLYGON_PROBLEM_ARN"
    ]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "contestId": contestid,
            "problemName": problemname,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_CREATE_POLYGON_PROBLEM_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    return body_dict


def commit_changes(contestid, problemidx):
    CHROMIUM_POLYGON_COMMIT_CHANGES_ARN = os.environ[
        "CHROMIUM_POLYGON_COMMIT_CHANGES_ARN"
    ]
    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "contestId": contestid,
            "problemIdx": problemidx,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_POLYGON_COMMIT_CHANGES_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    return body_dict["response"]
