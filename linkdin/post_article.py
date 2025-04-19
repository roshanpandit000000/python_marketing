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
import pyautogui
from urllib.parse import urlparse
import mimetypes
import subprocess
from PIL import Image
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Instagram credentials
USERNAME = "bellahararo@gmail.com"
PASSWORD = "Google@ccount@123!@#"

# Setup WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # <- This line keeps Chrome open

driver = webdriver.Chrome(service=service, options=options)
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
MAX_POSTS = int(input("Enter the number of posts to submit: "))
products = products[SKIP_COUNT:]


EMOJI_PATTERN = re.compile(
    "["
    "\U00010000-\U0010ffff"  # Match characters outside the BMP
    "]+",
    flags=re.UNICODE,
)


def extract_text_with_links(html):

    soup = BeautifulSoup(html, "html.parser")

    # Step 1: Replace <a> with "text (link)"
    for a in soup.find_all("a"):
        href = a.get("href")
        text = a.get_text(strip=True)
        if href:
            a.replace_with(f"{text} ({href})")
        else:
            a.unwrap()

    # Step 2: Replace <br> tags with newline
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Step 3: Get all text (no HTML)
    raw_text = soup.get_text()

    # Step 4: Normalize multiple newlines
    cleaned_text = re.sub(r"\n+", "\n", raw_text)

    # Step 5: Optional - remove emojis or unsupported Unicode
    safe_text = "".join(c for c in cleaned_text if ord(c) <= 0xFFFF)

    # Trim leading/trailing whitespace
    return safe_text.strip()


try:
    driver.get("https://www.linkedin.com/login")
    time.sleep(4)  # Wait for initial content to load

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    for index, selected_products in enumerate(products, start=1):
        if index > MAX_POSTS:
            print(f"\nReached the limit of {MAX_POSTS} posts. Exiting loop.")
            break

        total = len(products)
        print(
            f"\n=== Submitting post {index} of {total}: {selected_products.get('title', 'Untitled')} ==="
        )

        image_url = selected_products.get("images", "Untitled")
        image_path = os.path.abspath("cover_image.jpg")

        with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)
            print("Image is saveda")

        try:
            driver.get(
                "https://www.linkedin.com/article/new/?author=urn%3Ali%3Afsd_company%3A102952256"
            )
            time.sleep(2)  # Wait for initial content to load

            upload_image = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Upload from computer']")
                )
            )
            upload_image.click()
            time.sleep(2)
            print(image_path)
            time.sleep(1)  # Slight delay for focus
            pyautogui.write(image_path)
            time.sleep(1)  # Give dialog time to fully appear
            pyautogui.press("enter")
            time.sleep(2)
            print(f"Send 'upload_image' Input")
            upload_next = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Next']")
                )
            )
            upload_next.click()
            print(f"Click 'upload_next'")
            time.sleep(2)
            title = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//textarea[@placeholder='Title']")
                )
            )
            title.click()
            title_text = selected_products.get("title", "Untitled")
            title.send_keys(title_text)
            print("title Send Success")
            time.sleep(2)

            description = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@contenteditable='true']")
                )
            )
            description.click()
            html_data = selected_products.get("mainDescription", "Untitled")
            plain_text_description = extract_text_with_links(html_data)
            time.sleep(1)
            description.send_keys(plain_text_description)
            print("Description Send Success")
            time.sleep(2)

            next_article = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button//span[text()='Next']")
                )
            )
            next_article.click()
            time.sleep(1)

            text_input = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@data-placeholder='Tell your network what your article is about…']",
                    )
                )
            )
            text_input.click()
            short_desc = selected_products.get("shortDescription", "Untitled")
            pyperclip.copy(short_desc)
            text_input.send_keys(Keys.CONTROL + "v")
            text_input.send_keys(Keys.ENTER)
            pyperclip.copy(
                "#HairExtensions  #HairGoals  #LongHairDontCare  #HairTransformation  #HairInspo  #HairMagic  #LuxuryHair #ClipInExtensions  #TapeInExtensions  #SewInExtensions  #MicroLinkExtensions  #HaloExtensions  #FusionExtensions  #HandTiedExtensions"
            )
            text_input.send_keys(Keys.CONTROL + "v")
            time.sleep(1)

            publish = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button//span[text()='Publish']",
                    )
                )
            )
            publish.click()

            time.sleep(5)

        except Exception as e:
            print(
                f"Error submitting article {index} ({selected_products.get('name')}): {e}\n"
            )

except Exception as e:
    print(f"Login failed: {e}")
    driver.quit()
    exit()

time.sleep(5)  # Wait for the page to load before closing the driver
