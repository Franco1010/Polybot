import json
import utils
import asyncio
from clickMenu.menu import cli


def lambda_handler(event, context):
    print(event, context)
    print("received command: ", event["queryStringParameters"]["command"].split())

    utils.Logger.startBotStdout()

    try:
        asyncio.get_event_loop().run_until_complete(
            cli(
                event["queryStringParameters"]["command"].split(), standalone_mode=False
            )
        )
    except Exception as e:
        print(e)

    response = utils.Logger.stopBotStdout()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": response}),
    }
