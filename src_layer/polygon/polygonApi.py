import logging
import aiohttp
from . import endpoints as URL
from . import utils
import time
import hashlib
import random
import string
import boto3
import json
from urllib.parse import urlencode, quote
import requests
import uuid
import os

BUCKET = os.environ["BUCKET"]
PACKAGES_PATH = os.environ["PACKAGES_PATH"]

s3 = boto3.client("s3")

logger = logging.getLogger(__name__)

secrets_client = boto3.client("secretsmanager")
secret_value = secrets_client.get_secret_value(SecretId="api/polygon")
apiPolygonSecret = json.loads(secret_value["SecretString"])


def make_from_dict(namedtuple_cls, dict_):
    field_vals = [dict_.get(field) for field in namedtuple_cls._fields]
    return namedtuple_cls._make(field_vals)


def prepare_url(parameters_original, method_name):
    sec = str(int(time.time()))
    # First, copy the dictionary, so that you do not modify user's dictionary
    parameters = parameters_original.copy()
    # Add "time" and "apiKey" parameter
    parameters["time"] = sec
    parameters["apiKey"] = apiPolygonSecret["key"]
    # Add "problemproblemId" parameter only if it is a prob
    # if not (method_name == "problems.list" or method_name == "contest.problems"):
    #     parameters["problemId"] = PROBLEM_ID

    # Extract all keys of the dictionary
    keys = list(parameters.keys())

    # Sort all the keys
    keys.sort()

    # Create the parameters encoding
    common_part = method_name + "?"
    common_part_escaped = common_part

    # Concatenate the parameters in sorted order
    first = True
    for key in keys:
        if not first:
            common_part_escaped += "&"
            common_part += "&"

        value = parameters[key]
        if isinstance(value, str):
            value = value.encode("utf-8")
        else:
            value = str(value).encode("utf-8")

        common_part_escaped += key + "=" + quote(value)
        common_part += key + "=" + str(parameters[key])
        first = False

    rand_prefix = generate_random_prefix(6)
    to_hash = rand_prefix + "/" + common_part + "#" + apiPolygonSecret["secret"]
    hashed_string = create_sha512_hash(to_hash)
    request_url = (
        URL.BASE_URL + common_part_escaped + "&apiSig=" + rand_prefix + hashed_string
    )
    return request_url


def generate_random_prefix(string_length):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(string_length))


def create_sha512_hash(s):
    return hashlib.sha512(s.encode("utf-8")).hexdigest()


async def make_api_call(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json(content_type="text/html")
                if "result" in data:
                    return data["result"]
            else:
                return None


async def list_problems():
    params = {}
    url = prepare_url(params, URL.PROBLEMS_LIST_EP)
    resp = await make_api_call(url)
    return [make_from_dict(utils.Problem, problems_dict) for problems_dict in resp]


async def info(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_INFO_EP)
    resp = await make_api_call(url)
    if resp == None:
        return None
    return make_from_dict(utils.ProblemInfo, resp)


async def update_info(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_UPDATE_INFO_EP)
    resp = await make_api_call(url)


async def statements(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_STATEMENTS_EP)
    resp = await make_api_call(url)
    if resp == None:
        return None
    res = []
    for language, statement in resp.items():
        statement["lang"] = language
        res.append(make_from_dict(utils.Statement, statement))
    return res


async def statement_resources(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_STATEMENT_RESOURCES_EP)
    resp = await make_api_call(url)
    files = [make_from_dict(utils.File, file) for file in resp]
    for file in files:
        file["ResourceAdvancedProperties"] = make_from_dict(
            utils.ResourceAdvancedProperties, file["ResourceAdvancedProperties"]
        )
    return files


async def save_statement_resources():
    params = {}
    url = prepare_url(params, URL.PROBLEM_SAVE_STATEMENT_RESOURCE_EP)


async def checker(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_CHECKER_EP)
    resp = await make_api_call(url)
    return resp


async def validator(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_VALIDATOR_EP)
    resp = await make_api_call(url)
    return resp


async def interactor(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_INTERACTOR_EP)
    resp = await make_api_call(url)


async def files(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_FILES_EP)
    resp = await make_api_call(url)
    files = []
    for file in resp["resourceFiles"]:
        files.append(make_from_dict(utils.File, file))
    for file in resp["sourceFiles"]:
        files.append(make_from_dict(utils.File, file))
    for file in resp["auxFiles"]:
        files.append(make_from_dict(utils.File, file))
    return files


async def solutions(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_SOLUTIONS_EP)
    resp = await make_api_call(url)
    if resp == None:
        return None
    return [make_from_dict(utils.Solution, solutions_dict) for solutions_dict in resp]


async def tests(problemId, testset):
    params = {"problemId": problemId, "testset": testset}
    url = prepare_url(params, URL.PROBLEM_TESTS_EP)
    resp = await make_api_call(url)
    if resp == None:
        return None
    return [make_from_dict(utils.Test, test_dict) for test_dict in resp]


async def set_checker(problemId, checker):
    params = {"problemId": problemId, "checker": checker}
    url = prepare_url(params, URL.PROBLEM_SET_CHECKER_EP)
    resp = await make_api_call(url)
    return resp


async def set_validator(problemId, validator):
    params = {"problemId": problemId, "validator": validator}
    url = prepare_url(params, URL.PROBLEM_SET_VALIDATOR_EP)
    resp = await make_api_call(url)
    return resp


async def packages(problemId):
    params = {"problemId": problemId}
    url = prepare_url(params, URL.PROBLEM_PACKAGES_EP)
    resp = await make_api_call(url)
    if resp == None:
        return None
    return [make_from_dict(utils.Package, pack_dict) for pack_dict in resp]


async def contest(contestId):
    params = {"contestId": contestId}
    url = prepare_url(params, URL.CONTEST_PROBLEMS_EP)
    resp = await make_api_call(url)
    if resp is None:
        return None
    problems = []
    for letter, problem in resp.items():
        problem["letter"] = letter
        problems.append(make_from_dict(utils.Problem, problem))
    return problems


def download_package(problemId, packageId):
    params = {"problemId": problemId, "packageId": packageId}
    url = prepare_url(params, URL.PROBLEM_PACKAGE_EP)
    session = requests.Session()

    response = session.get(url, stream=True, allow_redirects=True)
    response.raise_for_status()

    s3_key = "{}/{}/{}".format(PACKAGES_PATH, str(uuid.uuid4()), "package")

    head_response = session.head(url, allow_redirects=True)
    content_type = head_response.headers.get("Content-Type", "application/octet-stream")

    print("contentType: ", content_type)

    with response as part:
        part.raw.decode_content = True
        conf = boto3.s3.transfer.TransferConfig(
            multipart_threshold=10000, max_concurrency=4
        )
        s3.upload_fileobj(
            part.raw,
            BUCKET,
            s3_key,
            Config=conf,
            ExtraArgs={"ContentType": content_type},
        )
    return s3_key


async def save_solution(problemId, name, file, tag):
    params = {"problemId": problemId, "name": name, "file": file, "tag": tag}
    url = prepare_url(params, URL.PROBLEM_SAVE_SOLUTION_EP)
    resp = await make_api_call(url)
    return resp


async def save_test(problemId, testset, testIndex, testInput):
    params = {
        "problemId": problemId,
        "testset": testset,
        "testIndex": testIndex,
        "testInput": testInput,
    }
    url = prepare_url(params, URL.PROBLEM_SAVE_TEST_EP)
    resp = await make_api_call(url)
    return resp


async def save_statement(problemId, lang, name, legend, input, output):
    params = {
        "problemId": problemId,
        "lang": lang,
        "name": name,
        "legend": legend,
        "input": input,
        "output": output,
    }
    url = prepare_url(params, URL.PROBLEM_SAVE_STATEMENT_EP)
    resp = await make_api_call(url)
    return resp
