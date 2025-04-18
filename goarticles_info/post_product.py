import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import requests


# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# API Endpoint for Articles
API_URL = "https://bellahararo.com/api/products"
response = requests.get(API_URL)
data = response.json()
products = data.get("allproducts", [])

# Exit if no articles
if not products:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()

SKIP_COUNT = int(input("Enter number of posts to skip: "))
products = products[SKIP_COUNT:]


EMOJI_PATTERN = re.compile(
    "["
    "\U00010000-\U0010ffff"  # Match characters outside the BMP
    "]+",
    flags=re.UNICODE,
)


for index, selected_products in enumerate(products, start=1):
    total = len(products)
    print(
        f"\n=== Submitting post {index} of {total}: {selected_products.get('name', 'Untitled')} ==="
    )

    try:
        driver.get("https://www.goarticles.info/post-story")
        time.sleep(5)  # Wait for initial content to load

        source_url = wait.until(EC.presence_of_element_located((By.ID, "source")))
        source_url.click()
        source_url.send_keys(Keys.CONTROL + "a")
        source_url.send_keys(Keys.DELETE)
        time.sleep(1)
        link = "https://bellahararo.com/shop/" + selected_products.get("slug", "")
        source_url.send_keys(link)
        print(f"Send 'Sources URL' Input")
        time.sleep(2)

        continue_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Continue']"))
        )
        continue_button.click()
        print("Clicked continue button")
        time.sleep(2)

        category_option = wait.until(
            EC.presence_of_element_located((By.ID, "category"))
        )
        category_option.click()

        education = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//ul[@aria-labelledby]//li[text()='Education']")
            )
        )
        education.click()
        print("Select Education")
        time.sleep(1)

        tags = wait.until(EC.presence_of_element_located((By.ID, "tags")))
        tags.click()
        time.sleep(1)
        tags.send_keys(
            "Weft Hair, Hair Extension, I-Tip, Long Hair, Bella Hararo, Machine Weft"
        )
        print("send Tags successfull")

        time.sleep(1)

        description = wait.until(EC.presence_of_element_located((By.ID, "description")))
        description.click()
        time.sleep(1)
        description.send_keys(selected_products.get("shortDescription", ""))
        time.sleep(1)
        print("Send Description Successfull")

        submit = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Submit']"))
        )
        submit.click()
        print("All inputs filled successfully!")
        time.sleep(5)

        # driver.quit()

    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_products.get('name')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
