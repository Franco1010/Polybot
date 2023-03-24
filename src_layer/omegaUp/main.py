import omegaup.api
import sys
import os
import math
from datetime import datetime, timedelta
import time
import boto3
import json

def createContest():
    contest_class = omegaup.api.Contest(client=client_class)
    start_time=datetime.datetime(2023, 4, 25, 10, 0)
    print(start_time)
    end_time=datetime.datetime(2023, 4, 25, 15, 0)
    timeOmega = omegaup.api.Time(client=client_class)
    print(dir(omegaup.api.Time.get))
    print(timeOmega.get().time)
    print(datetime.datetime.now().timestamp())
    print(start_time.timestamp())
    print(start_time)
    unix_start_time = start_time.timestamp()
    unix_end_time = end_time.timestamp()
    fb = "none"
    languages = 'java,cpp17-gcc'
    contests = contest_class.adminList()
    contest = contests.contests[0]
    print(contest.alias)
    x = contest_class.update(window_length=300, contest_alias="test69", title="Test 69", description="Description test", start_time=start_time, finish_time=unix_end_time, scoreboard=0, points_decay_factor = DEFAULT.POINTS_DECAY_FACTOR, submissions_gap = DEFAULT.SUBMISSION_GAP, penalty=DEFAULT.PENALTY, feedback=DEFAULT.FEEDBACK, penalty_type=DEFAULT.PENALTY_TYPE, languages=DEFAULT.LANGUAGES)
    print(x)
#    def create(
#	self,
#	*,
#	admission_mode: Optional[Any] = None,
#	alias: Optional[Any] = None,
#	check_plagiarism: Optional[bool] = None,
#	contest_for_teams: Optional[bool] = None,
#	description: Optional[Any] = None,
#	feedback: Optional[Any] = None,
#	finish_time: Optional[Any] = None,
#	languages: Optional[Any] = None,
#	needs_basic_information: Optional[bool] = None,
#	partial_score: Optional[bool] = None,
#	penalty: Optional[Any] = None,
#	penalty_calc_policy: Optional[Any] = None,
#	penalty_type: Optional[Any] = None,
#	points_decay_factor: Optional[Any] = None,
#	problems: Optional[str] = None,
#	requests_user_information: Optional[Any] = None,
#	score_mode: Optional[str] = None,
#	scoreboard: Optional[Any] = None,
#	show_scoreboard_after: Optional[Any] = None,
#	start_time: Optional[Any] = None,
#	submissions_gap: Optional[Any] = None,
#	teams_group_alias: Optional[str] = None,
#	title: Optional[Any] = None,
#	window_length: Optional[int] = None,
#	files_: Optional[Mapping[str, BinaryIO]] = None,
#	check_: bool = True,
#	timeout_: datetime.timedelta = datetime.timedelta(seconds=60)
#) -> None:

 

def main():
    secrets_client = boto3.client("secretsmanager")
    secret_value = secrets_client.get_secret_value(SecretId="account/omegaup")
    account = json.loads(secret_value["SecretString"])
    print(account["username"])
    print(account["password"])
    return
    username, password = get_credentials_from_file("login.txt")
    client_class = omegaup.api.Client(username=username, password=password)
    contest_class = omegaup.api.Contest(client=client_class)
    run_class = omegaup.api.Run(client=client_class)
    problemset_class = omegaup.api.Problemset(33527)
    problem_class = omegaup.api.Problem(client_class)
    contests = contest_class.adminList()
    contest = contests.contests[0]
    print(contest)
    print(contest.languages)
    createContest(client_class)
    return
    #print(dir(contest_class))
    alias = contest.alias
    #print(alias)
    #print(contest.title)
    #print(dir(contest))
    problems = contest_class.problems(contest_alias=alias)
    problem = problems.problems[0]
    print(dir(problem))
    print(problem.title)
    problem.title = "d"
    #00d937df457f551f5feb157bf6979eb23eed1b9d
    #cc1701df3065d647350adc2457cdcc57510e2b98
    #ffc3a8888401a3354b844c7992e941a72e3cecad
    #2553b17ce08d5bd41877a9b10c261d2122f60e7a
    #2553b17ce08d5bd41877a9b10c261d2122f60e7a
    #print(dir(problem))
    alias = "Parindromos"
    commitV = "cc1701df3065d647350adc2457cdcc57510e2b98"
    update_published="ffc3a8888401a3354b844c7992e941a72e3cecad"
    x = problem_class.selectVersion(commit=commitV, problem_alias=alias)
    print(x)
    #print(problem.alias)
    #print(problem.commit)
    #print(dir(problem.versions.published))
    #print(problem.versions.published)
    print(problem.commit)
    print("Hola")

if __name__ == "__main__":
    test = "2023-04-29T20:00"
    ejemplo = datetime.fromisoformat(test)
    x = timedelta(minutes=300)
    print(ejemplo)
    print(ejemplo + timedelta(minutes=300))
    #main()