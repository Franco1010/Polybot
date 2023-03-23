import os
import boto3
import os
import json
import sys
import uuid
import requests


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append("../")
from webDriver import WebDriver

POLYGON_WEBSITE = os.environ["POLYGON_WEBSITE"]
BUCKET = os.environ["BUCKET"]
PACKAGES_PATH = os.environ["PACKAGES_PATH"]

s3 = boto3.client("s3")

secrets_client = boto3.client("secretsmanager")
secret_value = secrets_client.get_secret_value(SecretId="account/polygon")
accountPolygonSecret = json.loads(secret_value["SecretString"])


def downloadPackage(contestId):
    webDriver = WebDriver()
    driver = webDriver.getDriver()

    # LOGIN

    driver.get(POLYGON_WEBSITE + "login")
    wait = WebDriverWait(driver, 120)
    loginForm = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "enterForm")))
    username_input = driver.find_element(By.NAME, "login")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(accountPolygonSecret["login"])
    password_input.send_keys(accountPolygonSecret["password"])
    checkbox = driver.find_element(By.NAME, "attachSessionToIp")
    if checkbox.is_selected():
        checkbox.click()
    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()

    ccid_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='ccid'][@value]"))
    )
    ccid_value = ccid_input.get_attribute("value")

    # GO TO CONTEST PAGE

    driver.get(
        POLYGON_WEBSITE
        + "contest?"
        + "contestId={}".format(contestId)
        + "&ccid={}".format(ccid_value)
    )

    download_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a.noSessionLink.contestDownloadLink")
        )
    )

    download_url = download_button.get_attribute("href")
    print(download_url)

    # copy cookies
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])

    headers = {"User-Agent": driver.execute_script("return navigator.userAgent;")}
    session.headers.update(headers)

    response = session.get(download_url, stream=True, allow_redirects=True)
    response.raise_for_status()

    s3_key = "{}/{}/{}".format(PACKAGES_PATH, str(uuid.uuid4()), "full_package")

    head_response = session.head(download_url, allow_redirects=True)
    content_type = head_response.headers.get("Content-Type", "application/octet-stream")

    print("contentType: ", content_type)

    with response as part:
        part.raw.decode_content = True
        conf = boto3.s3.transfer.TransferConfig(
            multipart_threshold=10000, max_concurrency=4
        )
        s3.upload_fileobj(
            part.raw,
            BUCKET,
            s3_key,
            Config=conf,
            ExtraArgs={"ContentType": content_type},
        )

    driver.close()
    return s3_key


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)
    response = downloadPackage(event["queryStringParameters"]["contestId"])
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": response}),
    }
