import sys
import click
from . import contest
import omegaUp.omegaUpApi as OmegaUpApi


@click.group()
@click.pass_context
async def omegaUp(ctx):
    pass


@omegaUp.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(omegaUp.get_help(ctx))

    
omegaUp.add_command(contest.contest)


