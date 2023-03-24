import os
import boto3
import os
import json
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

sys.path.append("../")
from webDriver import WebDriver

POLYGON_WEBSITE = os.environ["POLYGON_WEBSITE"]

secrets_client = boto3.client("secretsmanager")
secret_value = secrets_client.get_secret_value(SecretId="account/polygon")
accountPolygonSecret = json.loads(secret_value["SecretString"])


def createPolygonContest(contestName, contestLocation, contestDate):
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

    # GO TO CONTEST CREATION PAGE

    driver.get(POLYGON_WEBSITE + "cc?" + "ccid={}".format(ccid_value))

    # Find the form elements
    name_input = wait.until(EC.presence_of_element_located((By.NAME, "name")))
    location_input = wait.until(EC.presence_of_element_located((By.NAME, "location")))
    date_input = wait.until(EC.presence_of_element_located((By.NAME, "date")))
    main_language_select = wait.until(
        EC.presence_of_element_located((By.NAME, "language"))
    )
    select_main_language = Select(main_language_select)

    # Fill in the fields with the desired values
    name_input.send_keys(contestName)
    if contestLocation is not None:
        location_input.send_keys(contestLocation)
    if contestDate is not None:
        date_input.send_keys(contestDate)
    select_main_language.select_by_value(
        "english"
    )  # Replace 'english' with the value you want

    # Find and submit the form
    submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
    submit_button.click()

    wait.until(EC.presence_of_element_located((By.ID, "top-messagebox")))
    response = wait.until(EC.visibility_of_element_located((By.ID, "top-messagebox")))
    response = response.text

    first_row = driver.find_element_by_css_selector(
        "table.grid.tablesorter.contest-list-grid tbody tr"
    )
    contestId = first_row.find_elements_by_css_selector("td")[1].text

    driver.close()
    return {"response": response, "contestId": contestId}


def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)
    params = event["queryStringParameters"]
    response = createPolygonContest(
        contestName=params["name"],
        contestLocation=params["location"],
        contestDate=params["date"],
    )
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }
