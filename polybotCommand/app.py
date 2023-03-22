import json
import utils
import asyncio
from clickMenu.menu import cli
from clickMenu.setup import setup
import awsUtils.dynamoSpacesDB as spacesDB


def has_group(id, app):
    res = spacesDB.query(id, app)
    return len(res) > 0


def lambda_handler(event, context):
    print(event, context)
    print("received command: ", event["queryStringParameters"]["command"].split())

    context_extra = {
        "spaceId": event["queryStringParameters"]["id"],
        "spaceApp": event["queryStringParameters"]["app"],
    }

    commandsGroup = (
        cli
        if has_group(
            event["queryStringParameters"]["id"], event["queryStringParameters"]["app"]
        )
        else setup
    )

    # starts file logger
    utils.Logger.startBotStdout()

    try:
        asyncio.get_event_loop().run_until_complete(
            commandsGroup(
                event["queryStringParameters"]["command"].split(),
                prog_name="!",
                standalone_mode=False,
                obj=context_extra,
            )
        )
    except Exception as e:
        print(e)

    # stops file logger and get contents
    response = utils.Logger.stopBotStdout()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": response}),
    }
