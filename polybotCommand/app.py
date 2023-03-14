import json
import boto3
import os
import uuid
from webdriver_screenshot import WebDriverScreenshot
import click
import utils

@click.group()
def cli():
    pass

s3 = boto3.client('s3')

BUCKET = os.environ['BUCKET']
S3WEB = os.environ['S3WEB']
SCREENSHOT_PATH = os.environ["SCREENSHOT_PATH"]

@cli.command()
@click.argument("url")
def screenshot(url):
    """Toma una captura de pantalla de una URL."""
 
    screenshot_file = "{}-{}".format(''.join(filter(str.isalpha, url)), str(uuid.uuid4()))
    driver = WebDriverScreenshot()
    driver.save_screenshot(url, '/tmp/{}-fixed.png'.format(screenshot_file), height=1024)
    driver.save_screenshot(url, '/tmp/{}-full.png'.format(screenshot_file))

    driver.close()

    ## Upload generated screenshot files to S3 bucket.
    fixedPath = '{}/{}-fixed.png'.format(SCREENSHOT_PATH, screenshot_file)
    fullPath = '{}/{}-full.png'.format(SCREENSHOT_PATH, screenshot_file)
    s3.upload_file(
        '/tmp/{}-fixed.png'.format(screenshot_file), 
        BUCKET, 
        fixedPath
    )
    s3.upload_file(
        '/tmp/{}-full.png'.format(screenshot_file), 
        BUCKET, 
        fullPath
    )
    click.echo("fixed: {}".format(utils.shortPublicS3Url(BUCKET, S3WEB, fixedPath)))
    click.echo("full: {}".format(utils.shortPublicS3Url(BUCKET, S3WEB, fullPath)))

@cli.command()
def help():
    cli.help()

def lambda_handler(event, context):
    print(event, context)
    print('received command: ', event["queryStringParameters"]["command"].split())

    utils.Logger.startBotStdout()

    try:
        cli(event["queryStringParameters"]["command"].split(), standalone_mode=False)
    except Exception as e:
        print(e)

    response = utils.Logger.stopBotStdout()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "response": response
        }),
    }
