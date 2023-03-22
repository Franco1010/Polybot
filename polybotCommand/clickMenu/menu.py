import click
import json
import boto3
import os
import utils
from . import problem
from . import contest

BUCKET = os.environ["BUCKET"]
S3WEB = os.environ["S3WEB"]
SCREENSHOT_PATH = os.environ["SCREENSHOT_PATH"]
CHROMIUM_SCREENSHOT_ARN = os.environ["CHROMIUM_SCREENSHOT_ARN"]


class CustomHelp(click.Group):
    def get_help(self, ctx):
        ctx.info_name = "!"
        return super(CustomHelp, self).get_help(ctx)


@click.group(cls=CustomHelp)
async def cli():
    pass


@cli.command()
async def help():
    """Show this message and exit."""

    ctx = click.Context(cli)
    click.echo(ctx.get_help())


@cli.command()
@click.argument("url")
async def screenshot(url):
    """Take a screenshot of an URL."""

    lambda_client = boto3.client("lambda")
    payload = {
        "queryStringParameters": {
            "url": url,
        }
    }
    response = lambda_client.invoke(
        FunctionName=CHROMIUM_SCREENSHOT_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    body_dict = json.loads(response_payload["body"])
    res = body_dict["response"]
    click.echo("fixed: {}".format(utils.shortPublicS3Url(BUCKET, S3WEB, res["fixed"])))
    click.echo("full: {}".format(utils.shortPublicS3Url(BUCKET, S3WEB, res["full"])))


cli.add_command(problem.problem)
cli.add_command(contest.contest)
