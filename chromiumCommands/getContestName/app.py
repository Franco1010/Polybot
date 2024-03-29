import os
import boto3
import os
import json
import sys


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append("../")
from webDriver import WebDriver

POLYGON_WEBSITE = os.environ["POLYGON_WEBSITE"]

secrets_client = boto3.client("secretsmanager")
secret_value = secrets_client.get_secret_value(SecretId="account/polygon")
accountPolygonSecret = json.loads(secret_value["SecretString"])


def getContestName(contestId):
    webDriver = WebDriver()
    driver = webDriver.getDriver()

    # LOGIN

    driver.get(POLYGON_WEBSITE + "login")
    wait = WebDriverWait(driver, 120)
    loginForm = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "enterForm")))
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    username_input.send_keys(accountPolygonSecret["login"])
    password_input.send_keys(accountPolygonSecret["password"])
    checkbox = wait.until(
        EC.presence_of_element_located((By.NAME, "attachSessionToIp"))
    )
    if checkbox.is_selected():
        checkbox.click()
    submit_button = wait.until(EC.presence_of_element_located((By.NAME, "submit")))
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

    contestName = (
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-name")))
    ).text

    driver.close()
    return {"contestName": contestName}


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)
    params = event["queryStringParameters"]
    response = getContestName(
        contestId=params["contestId"],
    )
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }
