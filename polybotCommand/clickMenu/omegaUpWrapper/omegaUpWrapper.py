import sys
import click
from . import contest
import omegaUpWrapper.omegaUpApi as OmegaUpApi


@click.group(name="omegaup")
@click.pass_context
async def omegaUpWrapper(ctx):
    pass


@omegaUpWrapper.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(omegaUpWrapper.get_help(ctx))


omegaUpWrapper.add_command(contest.contest)
