import sys
import click


@click.group()
def contest():
    pass


@contest.command()
def contests_list():
    pass


@contest.command()
def create_contest():
    pass


@contest.command()
@click.argument("contestId")
def add_contest(contestId):
    pass


@contest.command()
@click.argument("contestId")
def see_contest(contestId):
    pass
