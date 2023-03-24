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


def createPolygonProblem(contestId, problemName):
    problemName = "-".join(problemName.lower().split())
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

    # GO TO PROBLEM CREATION (IN-CONTEST) PAGE
    driver.get(
        POLYGON_WEBSITE
        + "contest/{}/cp?".format(contestId)
        + "ccid={}".format(ccid_value)
    )

    select_element = wait.until(EC.presence_of_element_located((By.ID, "index")))
    current_selection = select_element.find_element_by_css_selector(
        "option:checked"
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

    wait.until(EC.presence_of_element_located((By.ID, "top-messagebox")))
    response = wait.until(EC.visibility_of_element_located((By.ID, "top-messagebox")))
    response = response.text

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
