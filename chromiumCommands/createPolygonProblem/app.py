import os
import boto3
import os
import json
import sys


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

sys.path.append("../")
from webDriver import WebDriver

POLYGON_WEBSITE = os.environ["POLYGON_WEBSITE"]

secrets_client = boto3.client("secretsmanager")
secret_value = secrets_client.get_secret_value(SecretId="account/polygon")
accountPolygonSecret = json.loads(secret_value["SecretString"])


def createPolygonProblem(contestId, problemName):
    problemName = "-".join(problemName.lower().split())
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

    # GO TO PROBLEM CREATION (IN-CONTEST) PAGE
    driver.get(
        POLYGON_WEBSITE
        + "contest/{}/cp?".format(contestId)
        + "ccid={}".format(ccid_value)
    )

    select_element = wait.until(EC.presence_of_element_located((By.ID, "index")))
    current_selection = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#index option:checked"))
    ).text
    print(f"Current selection: {current_selection}")

    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    name_field.send_keys(problemName)

    create_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='submit'][name='submit']")
        )
    )
    create_button.click()

    def find_field_error(wait):
        try:
            fieldError = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "field-error"))
            )
            return fieldError.text
        except TimeoutException:
            return None

    def find_top_messagebox(wait):
        try:
            response_element = wait.until(
                EC.visibility_of_element_located((By.ID, "top-messagebox"))
            )
            return response_element.text
        except TimeoutException:
            return "Unknown error"

    response = find_field_error(WebDriverWait(driver, 5))
    if response:
        driver.close()
        return {"error": response}

    response = find_top_messagebox(wait)
    driver.close()
    return {
        "response": response,
        "problemName": problemName,
        "problemIdx": current_selection,
    }


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)
    params = event["queryStringParameters"]
    response = createPolygonProblem(
        contestId=params["contestId"],
        problemName=params["problemName"],
    )
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }
