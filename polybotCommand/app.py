import json
import boto3
import os
import logging
import uuid
from webdriver_screenshot import WebDriverScreenshot
import click
import sys

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/tmp/clickOutput.txt", "w")
   
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass

    def close(self):
        self.log.close()

original_stdout = sys.stdout

@click.group()
def cli():
    pass

s3 = boto3.client('s3')

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    response = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name
        },
        ExpiresIn=expiration
    )
    return response

@cli.command()
@click.argument("url")
def screenshot(url):
    """Toma una captura de pantalla de una URL."""
 
    screenshot_file = "{}-{}".format(''.join(filter(str.isalpha, url)), str(uuid.uuid4()))
    driver = WebDriverScreenshot()
    driver.save_screenshot(url, '/tmp/{}-fixed.png'.format(screenshot_file), height=1024)
    driver.save_screenshot(url, '/tmp/{}-full.png'.format(screenshot_file))

    driver.close()

    if all (k in os.environ for k in ('BUCKET','DESTPATH')):
        ## Upload generated screenshot files to S3 bucket.
        s3.upload_file('/tmp/{}-fixed.png'.format(screenshot_file), 
                    os.environ['BUCKET'], 
                    '{}/{}-fixed.png'.format(os.environ['DESTPATH'], screenshot_file))
        s3.upload_file('/tmp/{}-full.png'.format(screenshot_file), 
                    os.environ['BUCKET'], 
                    '{}/{}-full.png'.format(os.environ['DESTPATH'], screenshot_file))
        
    click.echo("fixed: {}".format(generate_presigned_url(os.environ["BUCKET"], '{}/{}-fixed.png'.format(os.environ['DESTPATH'], screenshot_file))))
    click.echo("full: {}".format(generate_presigned_url(os.environ["BUCKET"], '{}/{}-full.png'.format(os.environ['DESTPATH'], screenshot_file))))

@cli.command()
def help():
    cli.help()

def lambda_handler(event, context):
    print(event, context)
    print('received command: ', event["queryStringParameters"]["command"].split())

    response = "NoResponse"

    sys.stdout = Logger()
    try:
        cli(event["queryStringParameters"]["command"].split(), standalone_mode=False)
    except Exception as e:
        print(e)
    sys.stdout.close()
    sys.stdout = original_stdout

    with open('/tmp/clickOutput.txt', 'r') as file: 
        response = file.read()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "response": response
        }),
    }
