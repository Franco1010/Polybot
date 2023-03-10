import json

# import requests


def lambda_handler(event, context):
    print(event, context)
    response = "No command"
    if event["queryStringParameters"] is not None:
        response = event["queryStringParameters"]["command"]
    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": response
        }),
    }
