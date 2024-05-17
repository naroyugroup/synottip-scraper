from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import json
import consts
import time
 
service = Service(executable_path="chromedriver.exe")
browser = uc.Chrome(service=service)
browser.get("https://sport.synottip.cz/zapasy?filter=7&timeDate=Today")

time.sleep(2)

# Log In

emailInput = browser.find_element(By.XPATH, "//input[@name='login']")
emailInput.send_keys(consts.Synopttip["email"])

passwordInput = browser.find_element(By.XPATH, "//input[@name='password']")
passwordInput.send_keys(consts.Synopttip["password"])

logInButton = browser.find_element(By.XPATH, "//button[@data-role='login__submit']")
logInButton.click()

time.sleep(2)

matches = browser.find_elements(By.XPATH, "//div[@data-test-role='event-list__item']")

matchData = []

for match in matches:

    # Extract match date
    date = match.find_element(By.XPATH, "./div[2]")
    dateValue = date.text.replace("\n", " ").replace(" ", " ").strip()

    # Extract match title
    title = match.find_element(By.XPATH, "./div[1]/div/div[1]")
    titleText = title.get_attribute("textContent").replace(" ", " ").strip()

    # Extract odds
    oddsElements = match.find_elements(By.XPATH, ".//div[contains(@data-test-role, 'rate')]")
    odds = {}

    for oddsElement in oddsElements:
       bet = oddsElement.find_element(By.XPATH, "./div[1]")
       odd = oddsElement.find_element(By.XPATH, "./div[2]")
       odds[bet.get_attribute("textContent").replace(" ", " ").strip()] = odd.get_attribute("textContent").replace(" ", " ").strip()
        
    # Append match data to the list
    matchData.append({
        "title": titleText,
        "date":  dateValue,
        "odds": odds
    })

# Create a dictionary with match data
data = {"matches": matchData}

# Write data to a JSON file
with open("synottip-matches.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)

browser.quit()
