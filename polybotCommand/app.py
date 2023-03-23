import json
import utils
import asyncio
from clickMenu.menu import cli
from clickMenu.setup import setup
import awsUtils.dynamoSpacesDB as spacesDB


def get_group(id, app):
    res = spacesDB.query(id, app)
    if len(res) > 0:
        return res[0]["groupId"]
    else:
        return None


def lambda_handler(event, context):
    print(event, context)

    # Cargar el JSON del cuerpo de la solicitud
    request_data = json.loads(event["body"])

    print("received command: ", request_data["command"].split())

    request_data["groupId"] = get_group(
        request_data["callerCtx"]["space"]["id"],
        request_data["callerCtx"]["space"]["app"],
    )

    commandsGroup = cli if request_data["groupId"] != None else setup

    # starts file logger
    utils.Logger.startBotStdout()

    try:
        asyncio.get_event_loop().run_until_complete(
            commandsGroup(
                request_data["command"].split(),
                prog_name="!",
                help_option_names=["--help", "--h"],
                standalone_mode=False,
                obj=request_data,
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
