import sys
import click
import polygon.polygonApi as PolygonApi


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
