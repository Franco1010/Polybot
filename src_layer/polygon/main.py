import aiohttp
import asyncio
import endpoints as URL
import random
import string
import time
import hashlib
from urllib.parse import urlencode, quote
from util import *
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('POLYGON_API_KEY')
SECRET = os.getenv('POLYGON_SECRET')


def make_from_dict(namedtuple_cls, dict_):
    field_vals = [dict_.get(field) for field in namedtuple_cls._fields]
    return namedtuple_cls._make(field_vals)
def prepare_url(parameters_original, method_name):
    sec = str(int(time.time()))

    # First, copy the dictionary, so that you do not modify user's dictionary
    parameters = parameters_original.copy()

    # Add "time" and "apiKey" parameter
    parameters["time"] = sec
    parameters["apiKey"] = API_KEY

    # Add "problemId" parameter only if it is a prob
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
    to_hash = rand_prefix + "/" + common_part + "#" + SECRET
    hashed_string = create_sha512_hash(to_hash)
    request_url = URL.BASE_URL + common_part_escaped + "&apiSig=" + rand_prefix + hashed_string
    return request_url

def generate_random_prefix(string_length):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(string_length))


def create_sha512_hash(s):
    return hashlib.sha512(s.encode("utf-8")).hexdigest()

async def make_api_call(url):
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json(content_type='text/html')
                if 'result' in data:
                    return data['result']
                return "ok"
                data = await response.json(content_type='text/html')
                print(data)
                return data['result']
            else:
                return None

async def main():
    a = dict()
    a["problemId"]='253319'
    a['validator']='generator.cpp'
    url = prepare_url(a,URL.PROBLEM_SET_VALIDATOR_EP)
    data = await make_api_call(url)
    print(data)

    # if data is not None:
    #     print(data)
    # else:
    #     print("Error en la llamada a la API")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
