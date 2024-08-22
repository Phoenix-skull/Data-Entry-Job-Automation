import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException as StaleElement
from selenium.common.exceptions import ElementNotInteractableException as NotInteractable

rental_listings_url = "https://appbrewery.github.io/Zillow-Clone/"
reference_form = "https://docs.google.com/forms/d/1AZ5ZenivDv3nCtBXlHXm388SM7XklOZmRndt5z9pnCw/edit"

response = requests.get(url=rental_listings_url).text

soup = BeautifulSoup(markup=response, features="html.parser")
property_links = soup.find_all(name="a", class_="property-card-link")
property_links = [a["href"] for a in property_links]

property_prices = soup.select(selector='span[data-test="property-card-price"]')
property_prices = [price.text.strip("+/mo, +1bd") for price in property_prices]

property_addresses = soup.select('address[data-test="property-card-addr"]')
property_addresses = [address.text.strip("\n, ").replace(" | ", " ")
                      for address in property_addresses]


driver = webdriver.Edge()
driver.get(reference_form)

inputs = driver.find_elements(By.CSS_SELECTOR, "input.whsOnd")

for i in range(0, len(property_links)):
    time.sleep(0.2)
    try:
        inputs[0].send_keys(property_addresses[i])
    except StaleElement:
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.whsOnd")
        inputs[0].send_keys(property_addresses[i])
    inputs[1].send_keys(property_prices[i])
    inputs[2].send_keys(property_links[i])
    #Clicks the submit button
    driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Submit"]').click()
    # #Submit another response
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
driver.quit()
