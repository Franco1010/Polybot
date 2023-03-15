import sys
import click


sys.path.append("../")
from screenshot import take as take_screenshot


class CustomHelp(click.Group):
    def get_help(self, ctx):
        ctx.info_name = "!"
        return super(CustomHelp, self).get_help(ctx)


@click.group(cls=CustomHelp)
def cli():
    pass


@cli.command()
def help():
    """Show this message and exit."""

    ctx = click.Context(cli)
    click.echo(ctx.get_help())


@cli.command()
@click.argument("url")
def screenshot(url):
    """Take a screenshot of an URL."""

    res = take_screenshot(url)
    click.echo("fixed: {}".format(res["fixed"]))
    click.echo("full: {}".format(res["full"]))
