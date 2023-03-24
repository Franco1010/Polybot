import click
import json
import boto3
import os
import utils
import uuid
from tabulate import tabulate

import awsUtils.dynamoContestsDB as contestsDB
import awsUtils.dynamoContestRequestsDB as contestRequestDB
import omegaUpWrapper.omegaUpApi as OmegaUpApi


@click.group()
@click.pass_context
async def contest(ctx):
    pass


@contest.command()
@click.pass_context
async def help(ctx):
    """Show this message and exit."""
    click.echo(contest.get_help(ctx))


@contest.command()
@click.pass_context
@click.argument("contest_title", type=str)
@click.argument("contest_start", type=str)
@click.argument("contest_duration", type=int)
@click.option("--custom_id", type=str, help="Custom id for the contest")
@click.option("--description", type=str, help="Description of the contest")
@click.option(
    "--languages",
    type=str,
    help="Languages available in the contest 'c11-clang'|'c11-gcc'|'cat'|'cpp11-clang'|'cpp11-gcc'|'cpp17-clang'|'cpp17-gcc'|'cpp20-clang'|'cpp20-gcc'|'cs'|'go'|'hs'|'java'|'js'|'kj'|'kp'|'kt'|'lua'|'pas'|'py2'|'py3'|'rb'|'rs'|null",
)
@click.option(
    "--scoreboard",
    type=int,
    help="Integer representing the porcentage of time the scoreboard will be visible",
)
async def create(
    ctx,
    contest_title,
    contest_start,
    contest_duration,
    custom_id,
    description,
    languages,
    scoreboard,
):
    """Create contest test.\n
    contest_title: Title of the contest.\n
    contest_start: Start date of the contest in the ISO date format, YYYY-MM-DDTHH:mm.\n
    contest_duration: Integer of the duration in minutes.\n
    """
    contest_id = str(uuid.uuid4())[:22]
    if custom_id:
        contest_id = custom_id
    creation = OmegaUpApi.create_contest(
        contest_id,
        contest_title,
        contest_start,
        contest_duration,
        description,
        languages,
        scoreboard,
    )
    click.echo(creation)
    if creation == "Contest created":
        contestsDB.create_item(contest_id, "omegaUp", contest_title, ctx.obj["groupId"])


@contest.command(name="list")
@click.pass_context
async def contest_list(ctx):
    result = contestsDB.query_contests(ctx.obj["groupId"])
    if len(result):
        data = []
        for i in result:
            if i["source"] == "omegaUp":
                data.append([i["name"], i["id"]])
        table = (
            "```\n"
            + tabulate(data, headers=["Name", "Id"], tablefmt="pretty")
            + "\n```"
        )
        click.echo(table)
    else:
        click.echo("Your group doesn't have contests")


@contest.command()
@click.pass_context
@click.argument("contest_id", type=str)
@click.argument("username", nargs=-1)
async def add_user(ctx, contest_id, username):
    """Add user to a contest.\n
    contest_id: Id of the contest.
    username: Username of the contestant that will be added to the contest\n."""
    for user in username:
        click.echo(user + ":" + OmegaUpApi.add_user(contest_id, user))
