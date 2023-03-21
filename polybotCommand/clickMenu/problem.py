import sys
import click
import polygon.polygonApi as PolygonApi


@click.group()
def problem():
    pass


@problem.command()
@click.argument("contestid")
def create(contestid):
    pass


@problem.command()
@click.argument("contestid")
@click.argument("problemid")
async def see_info(contestid, problemid):
    res = await PolygonApi.info(problemId=problemid)
    click.echo(res)


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
def see_package(contestid, problemid, packageid):
    pass
