import omegaup.api
import sys
import os
import math
from datetime import datetime, timedelta
import time
import boto3
import json
from . import constants as DEFAULT

secrets_client = boto3.client("secretsmanager")
secret_value = secrets_client.get_secret_value(SecretId="account/omegaup")
account = json.loads(secret_value["SecretString"])
username = account["username"]
password = account["password"]
client_class = omegaup.api.Client(username=username, password=password)

def create_contest(contest_id, contest_title, contest_start, contest_duration, contest_description, contest_languages, contest_scoreboard):
    contest_class = omegaup.api.Contest(client=client_class)
    start_time=datetime.fromisoformat(contest_start)
    end_time=start_time + timedelta(minutes=contest_duration)
    unix_start_time = start_time.timestamp()
    unix_end_time = end_time.timestamp()
    alias = contest_id
    title = contest_title
    if(contest_description):
        description = contest_description
    else:
        description = "Contest named " + title + " with a duration of " + str(contest_duration) + " minutes."
    if(contest_languages):
        languages = contest_languages
    else:
        languages = DEFAULT.LANGUAGES
    if(contest_scoreboard):
        scoreboard = contest_scoreboard
    else:
        scoreboard = DEFAULT.SCOREBOARD
    contest_class.create(alias=alias, title=title, description=description, start_time=unix_start_time, finish_time=unix_end_time, scoreboard=scoreboard, points_decay_factor = DEFAULT.POINTS_DECAY_FACTOR, submissions_gap = DEFAULT.SUBMISSION_GAP, penalty=DEFAULT.PENALTY, feedback=DEFAULT.FEEDBACK, penalty_type=DEFAULT.PENALTY_TYPE, languages=languages)
    return "Contest created"