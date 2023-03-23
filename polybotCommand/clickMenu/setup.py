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
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(setup.get_help(ctx))


@setup.command()
@click.pass_context
async def create(ctx):
    """Create a new group and add this server to that group"""
    click.echo(ctx.obj)
    id = spacesDB.createItem(ctx.obj["spaceId"], ctx.obj["spaceApp"])
    click.echo(id)


@setup.command()
@click.pass_context
async def add():
    """Add this server to a group."""
