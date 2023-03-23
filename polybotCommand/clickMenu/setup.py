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
    id = spacesDB.create_item(
        ctx.obj["callerCtx"]["space"]["id"],
        ctx.obj["callerCtx"]["space"]["app"],
        ctx.obj["callerCtx"]["space"]["name"],
    )
    click.echo("Your server is now part of the group: " + str(id))
    click.echo(
        "You can now access our full menu",
    )


@setup.command()
@click.pass_context
async def add():
    """Add this server to a group."""
