import sys
import click
import awsUtils.dynamoRequestsDB as requestsDB
import awsUtils.dynamoSpacesDB as spacesDB
from tabulate import tabulate


@click.group()
@click.pass_context
async def about(ctx):
    """Show information about the group."""
    pass


@about.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(about.get_help(ctx))


@about.command()
@click.pass_context
async def id(ctx):
    """Show the group id."""
    click.echo("Your group ID is: " + ctx.obj["groupId"])


@about.command()
@click.pass_context
async def join_requests(ctx):
    """See all join requests to this group"""
    result = requestsDB.query(ctx.obj["groupId"])
    if len(result):
        data = [
            [
                r["requestId"],
                r["name"],
                r["space"],
                r["date"],
            ]
            for r in result
            if r["status"] == "pending"
        ]
        if len(data):
            table = (
                "```\n"
                + tabulate(
                    data,
                    headers=["RequestId", "Name", "Space", "Date"],
                    tablefmt="pretty",
                )
                + "\n```"
            )
            click.echo(table)
        else:
            click.echo("Your group doesn't have join requests")
    else:
        click.echo("Your group doesn't have join requests")


@about.command()
@click.argument("requestid")
@click.pass_context
async def authorize(ctx, requestid):
    """Authorize other servers to access the group."""
    result = requestsDB.query_request(ctx.obj["groupId"], requestid)
    if len(result) == 1 and result[0]["status"] == "pending":
        requestsDB.update_status(
            result[0]["groupId"], result[0]["requestId"], "authorized"
        )
        spacesDB.add_item(
            ctx.obj["groupId"],
            result[0]["server"],
            result[0]["space"],
            result[0]["name"],
        )
        click.echo("Request authorized")
    else:
        click.echo("Request not found")


@about.command()
@click.argument("requestid")
@click.pass_context
async def decline(ctx, requestid):
    """Authorize other servers to access the group."""
    result = requestsDB.query_request(ctx.obj["groupId"], requestid)
    if len(result) == 1 and result[0]["status"] == "pending":
        requestsDB.update_status(
            result[0]["groupId"], result[0]["requestId"], "declined"
        )
        click.echo("Request declined")
    else:
        click.echo("Request not found")


@about.command()
@click.pass_context
async def spaces(ctx):
    """Show all spaces in this group."""
    result = spacesDB.query_group(ctx.obj["groupId"])
    if len(result):
        data = [
            [
                r["name"],
                r["app"],
            ]
            for r in result
        ]
        if len(data):
            table = (
                "```\n"
                + tabulate(
                    data,
                    headers=[
                        "Name",
                        "App",
                    ],
                    tablefmt="pretty",
                )
                + "\n```"
            )
            click.echo(table)
        else:
            click.echo("Your group doesn't have spaces")
    else:
        click.echo("Your group doesn't have spaces")
