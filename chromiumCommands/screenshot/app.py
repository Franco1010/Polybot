import os
import uuid
import boto3
import os
import json
import sys

sys.path.append("../")
from webDriver import WebDriver

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET"]
S3WEB = os.environ["S3WEB"]
SCREENSHOT_PATH = os.environ["SCREENSHOT_PATH"]


def take(url):
    screenshot_file = "{}-{}".format(
        "".join(filter(str.isalpha, url)), str(uuid.uuid4())
    )
    driver = WebDriver()
    driver.save_screenshot(
        url, "/tmp/{}-fixed.png".format(screenshot_file), height=1024
    )
    driver.save_screenshot(url, "/tmp/{}-full.png".format(screenshot_file))

    driver.close()

    ## Upload generated screenshot files to S3 bucket.
    fixedPath = "{}/{}-fixed.png".format(SCREENSHOT_PATH, screenshot_file)
    fullPath = "{}/{}-full.png".format(SCREENSHOT_PATH, screenshot_file)
    s3.upload_file("/tmp/{}-fixed.png".format(screenshot_file), BUCKET, fixedPath)
    s3.upload_file("/tmp/{}-full.png".format(screenshot_file), BUCKET, fullPath)
    return {
        "fixed": fixedPath,
        "full": fullPath,
    }


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)
    response = take(event["queryStringParameters"]["url"])
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": response}),
    }
