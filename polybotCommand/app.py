import json

# import requests


def lambda_handler(event, context):
    print(event, context)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": event.body
        }),
    }
