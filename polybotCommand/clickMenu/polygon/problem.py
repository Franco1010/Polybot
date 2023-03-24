import sys
import click
import awsUtils.dynamoContestsDB as contestsDB
import polygon.polygonApi as PolygonApi
from tabulate import tabulate
import utils
import os


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
async def create(contestid):
    pass


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
async def see_statements(contestid, problemid):
    res = await PolygonApi.statements(problemId=problemid)
    click.echo(res)


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
async def see_files(contestid, problemid):
    res = await PolygonApi.files(problemId=problemid)
    click.echo(res)


def is_mine(groupId, contestId):
    res = contestsDB.query(contestId, "polygon")
    if len(res):
        if res[0]["groupId"] == groupId:
            return 2  # mine
        return 1  # owned
    return 0  # not owned