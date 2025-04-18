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
import os
import pyperclip
import tempfile
from urllib.parse import urlparse
import mimetypes
from PIL import Image


# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# API Endpoint for Articles
API_URL = "https://bellahararo.com/api/article"
response = requests.get(API_URL)
data = response.json()
products = data.get("articles", [])

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


def extract_text_with_links(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove all tags except <br>
    for tag in soup.find_all():
        if tag.name != "br":
            tag.unwrap()

    # Replace <br> with newline
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Get text and clean it
    raw_text = soup.get_text()

    # Remove multiple empty lines (more than one \n in a row becomes one)
    cleaned_text = re.sub(r"\n+", "\n", raw_text)

    # Strip unsupported Unicode (like emojis)
    safe_text = "".join(c for c in cleaned_text if ord(c) <= 0xFFFF)

    # Trim leading/trailing whitespace
    return safe_text.strip()


for index, selected_products in enumerate(products, start=1):
    total = len(products)
    print(
        f"\n=== Submitting post {index} of {total}: {selected_products.get('title', 'Untitled')} ==="
    )

    try:
        driver.get("https://flipboard.com/@bellahararo")
        time.sleep(2)  # Wait for initial content to load

        create_flip = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@data-vars-button-name='navbar-flip-compose']")
            )
        )
        create_flip.click()
        print(f"Send 'create_flip' Input")
        time.sleep(1)

        magazine = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//button[@data-vars-button-name='flip-compose-magazine'])[1]",
                )
            )
        )
        magazine.click()
        print(f"Send 'magazine' Input")
        time.sleep(1)

        # Upload the image
        Next = driver.find_element(
            By.XPATH,
            "(//button[@data-vars-button-name='submit'])",
        )
        Next.click()
        print("Click Next")
        time.sleep(1)

        # Upload the image
        Link = driver.find_element(
            By.XPATH,
            "(//button[@data-vars-button-name='flip-compose-add-url'])",
        )
        Link.click()
        print("Click Link")
        time.sleep(1)
        # Delete temp image
        # Upload the image
        Link_input = driver.find_element(
            By.XPATH,
            "(//input[@placeholder='Enter a URL to add to your new Flip'])",
        )
        Link_input.click()
        articel_slug = "https://bellahararo.com/articles/" + selected_products.get(
            "slug", "Untitled"
        )
        Link_input.send_keys(articel_slug)
        print("Send Link_input")
        time.sleep(2)
        # Try to delete the file safely with retries

        link_ok = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//button[@data-vars-button-name='add-preview-okay'])",
                )
            )
        )
        link_ok.click()
        time.sleep(1)

        post_find = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//button[@data-vars-button-name='remove-attachment'])")
            )
        )
        time.sleep(1)
        print("Post button click")

        try:
            print("post find Find")
            time.sleep(1)

            # Re-fetch the <select> element after the DOM update
            submit = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//button[@data-vars-button-name='submit'])")
                )
            )
            submit.click()
            time.sleep(1)
            print(f"Clicked 'Submit' Div")
        except Exception as e:
            print(f"Error adding tags: {e}")
        print("Magazine Done")
        time.sleep(1)

        print("post button CLicked")

        time.sleep(2)

    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_products.get('name')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
