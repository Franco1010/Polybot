import sys
import click
import awsUtils.dynamoContestsDB as contestsDB
import awsUtils.dynamoContestRequestsDB as contestRequestDB
import polygon.polygonApi as PolygonApi
from tabulate import tabulate


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
            break
    table = "```\n" + tabulate(data, tablefmt="pretty") + "\n```"
    click.echo(table)


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


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
@click.argument("packageid")
async def see_package(contestid, problemid, packageid):
    pass


def is_mine(groupId, contestId):
    res = contestsDB.query(contestId, "polygon")
    if len(res):
        if res[0]["groupId"] == groupId:
            return 2  # mine
        return 1  # owned
    return 0  # not owned