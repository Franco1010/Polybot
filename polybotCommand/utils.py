import random
import string
import sys
import boto3

s3 = boto3.client('s3')
original_stdout = sys.stdout

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
    @staticmethod
    def startBotStdout():
        sys.stdout = Logger()
    def stopBotStdout():
        sys.stdout.close()
        response = ''
        with open('/tmp/clickOutput.txt', 'r') as file: 
            response = file.read()
        sys.stdout = original_stdout
        return response

def generate_random_alphanumeric(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def generate_presigned_url(Bucket, Key, ExpiresIn=3600):
    response = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': Bucket,
            'Key': Key
        },
        ExpiresIn=ExpiresIn
    )
    return response

def shortPublicS3Url(Bucket, BucketWeb, Key):
    presignedUrl = generate_presigned_url(Bucket, Key)
    shortKey = 'public/{}'.format(generate_random_alphanumeric(10))
    s3.put_object(Bucket=Bucket, Key=shortKey, WebsiteRedirectLocation=presignedUrl)
    return "{}/{}".format(BucketWeb, shortKey)