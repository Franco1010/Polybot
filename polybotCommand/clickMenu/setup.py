import click
import json
import boto3
import os
import utils
import awsUtils.dynamoSpacesDB as spacesDB


@click.group()
@click.pass_context
async def setup(ctx):
    pass


@setup.command()
async def help():
    """Show this message and exit."""
    ctx = click.Context(setup)
    click.echo(ctx.get_help())


@setup.command()
@click.pass_context
async def create(ctx):
    click.echo(ctx.obj)
    id = spacesDB.createItem(ctx.obj["spaceId"], ctx.obj["spaceApp"])
    click.echo(id)


@setup.command()
@click.pass_context
async def add():
    """Take a screenshot of an URL."""
