import logging
import aiohttp
import endpoints as URL
import polygonApiError as Error
from util import *

logger = logging.getLogger(__name__)
_session = None

def make_from_dict(namedtuple_cls, dict_):
    field_vals = [dict_.get(field) for field in namedtuple_cls._fields]
    return namedtuple_cls._make(field_vals)

async def initialize():
    global _session
    _session = aiohttp.ClientSession()

async def _query_api(path, data=None):
    url = URL.BASE_URL + path
    try:
        logger.info(f'Querying Polygon API at {url} with {data}')
        # Explicitly state encoding (though aiohttp accepts gzip by default)
        headers = {'Accept-Encoding': 'gzip'}
        async with _session.post(url, data=data, headers=headers) as resp:
            try:
                respjson = await resp.json()
            except aiohttp.ContentTypeError:
                logger.warning(f'CF API did not respond with JSON, status {resp.status}.')
                raise Error.CodeforcesApiError
            if resp.status == 200:
                return respjson['result']
            comment = f'HTTP Error {resp.status}, {respjson.get("comment")}'
    except aiohttp.ClientError as e:
        logger.error(f'Request to CF API encountered error: {e!r}')
        raise Error.ClientError from e
    logger.warning(f'Query to CF API failed: {comment}')
    if 'limit exceeded' in comment:
        raise Error.CallLimitExceededError(comment)
    raise Error.TrueApiError(comment)

class Polygon:
    @staticmethod
    async def list():
        params = {}
        resp = await _query_api(URL.PROBLEMS_LIST_EP,params)
        return [make_from_dict(Problem, problems_dict) for problems_dict in resp]
    async def info():
        params = {}
        resp = await _query_api(URL.PROBLEM_INFO_EP,params)
        return make_from_dict(ProblemInfo,resp)
    async def update_info():
        params = {}
        resp = await _query_api(URL.PROBLEM_UPDATE_INFO_EP,params)
    async def statements():
        params = {}
        resp = await _query_api(URL.PROBLEM_STATEMENTS_EP,params)
        return [[language, make_from_dict(Statement, statement)] for language,statement in resp]
    async def save_statement():
        params = {}
        resp = await _query_api(URL.PROBLEM_SAVE_STATEMENT_EP,params)
    async def statement_resources():
        params = {}
        resp = await _query_api(URL.PROBLEM_STATEMENT_RESOURCES_EP,params)
        files = [make_from_dict(File, file) for file in resp]
        for file in files:
            file['ResourceAdvancedProperties']=make_from_dict(ResourceAdvancedProperties, file['ResourceAdvancedProperties'])
        return files
    async def save_statement_resources():
        params = {}
        resp = await _query_api(URL.PROBLEM_SAVE_STATEMENT_RESOURCE_EP,params)
    async def problem_checker():
        params = {}
        resp = await _query_api(URL.PROBLEM_CHECKER_EP,params)
    async def problem_validator():
        params = {}
        resp = await _query_api(URL.PROBLEM_VALIDATOR_EP,params)
    async def problem_interactor():
        params = {}
        resp = await _query_api(URL.PROBLEM_INTERACTOR_EP,params)
    async def files():
        params = {}
        resp = await _query_api(URL.PROBLEM_FILES_EP,params)
        files=[]
        files.append([make_from_dict(File, file) for file in resp['ResourceFile']])
        files.append([make_from_dict(File, file) for file in resp['SourceFiles']])
        files.append([make_from_dict(File, file) for file in resp['AuxFiles']])
        for file in files:
            file['ResourceAdvancedProperties']=make_from_dict(ResourceAdvancedProperties, file['ResourceAdvancedProperties'])
        return files
    async def solutions():
        params = {}
        resp = await _query_api(URL.PROBLEM_SOLUTIONS_EP,params)
        return [make_from_dict(Solution, solutions_dict) for solutions_dict in resp]
    async def tests():
        params = {}
        resp = await _query_api(URL.PROBLEM_TESTS_EP,params)
        return [make_from_dict(Test, test_dict) for test_dict in resp]
    async def problem_set_checker():
        params = {}
        resp = await _query_api(URL.PROBLEM_SET_CHECKER_EP,params)

    