from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import requests  # Import for API requests
import json
import re


# Set up Chrome to use an existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=chrome_options)  # Attach to existing browser

driver.get("https://www.grammarly.com/paraphrasing-tool")

title = "Are you a PM short on time? You’re probably doing too much mental math."

try:
    wait = WebDriverWait(driver, 20)
    see_more_button = driver.find_element(
        By.XPATH, "//textarea[@placeholder='Type or paste your text here.']"
    )
    print("input Found")
    see_more_button.click()
    time.sleep(1)
    print("input Clicked")
    see_more_button.send_keys(title)
    time.sleep(1)
    print("input Send Text")
    click_paraphrase = driver.find_element(
        By.XPATH, "//button[contains(., 'Paraphrase')]"
    )
    see_more_button.click()
    time.sleep(2)
    print(f"DONE")
    time.sleep(4)
except Exception as e:
    print(f"Error clicking button for: {e}")
