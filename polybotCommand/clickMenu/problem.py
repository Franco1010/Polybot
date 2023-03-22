import sys
import click
import polygon.polygonApi as PolygonApi


@click.group()
async def problem():
    pass


@problem.command()
def help():
    """Show this message and exit."""
    ctx = click.Context(problem)
    click.echo(ctx.get_help())


@problem.command()
@click.argument("contestid")
async def create(contestid):
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
async def see_package(contestid, problemid, packageid):
    pass
