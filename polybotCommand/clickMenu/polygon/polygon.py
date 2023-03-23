import sys
import click
from . import problem
from . import contest


@click.group()
@click.pass_context
async def polygon(ctx):
    pass


@polygon.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(problem.get_help(ctx))


polygon.add_command(problem.problem)
polygon.add_command(contest.contest)