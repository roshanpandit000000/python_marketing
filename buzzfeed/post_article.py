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


for index, selected_products in enumerate(products, start=1):
    if index > MAX_POSTS:
        print(f"\nReached the limit of {MAX_POSTS} posts. Exiting loop.")
        break
    total = len(products)
    print(
        f"\n=== Submitting post {index} of {total}: {selected_products.get('title', 'Untitled')} ==="
    )

    try:
        driver.get("https://community.buzzfeed.com/post")
        time.sleep(2)  # Wait for initial content to load

        title = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@data-placeholder='Headline']")
            )
        )
        title.click()
        time.sleep(1)
        pyperclip.copy(selected_products.get("title", ""))
        title.send_keys(Keys.CONTROL + "v")
        print(f"Send 'Title' Input")
        time.sleep(1)

        subtitle = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@data-placeholder='Description']")
            )
        )
        subtitle.click()
        time.sleep(1)
        pyperclip.copy(selected_products.get("shortDescription", ""))
        subtitle.send_keys(Keys.CONTROL + "v")
        print(f"Send 'Subtitle' Input")
        time.sleep(1)

        article_title = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@placeholder='Start typing, drag an image, or paste a link or embed code']",
                )
            )
        )
        article_title.click()
        time.sleep(1)
        pyperclip.copy(selected_products.get("title", ""))
        article_title.send_keys(Keys.CONTROL + "v")
        time.sleep(1)
        article_title.send_keys(Keys.ENTER)
        print(f"Send 'Title' Input")
        time.sleep(2)

        description = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@data-placeholder='Add some text...']",
                )
            )
        )
        print("description Found")
        description.click()
        print("click description")
        html_description = selected_products.get("mainDescription", "")
        plain_text_description = extract_text_with_links(html_description)
        # print(plain_text_description)
        time.sleep(1)
        pyperclip.copy(plain_text_description)
        time.sleep(1)
        textarea = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@placeholder='Add some text...']",
                )
            )
        )
        print("copyed Clip")
        # textarea.click()
        # print("click again")
        textarea.send_keys(Keys.CONTROL + "v")
        time.sleep(1)
        print("Add Description Done")
        textarea.send_keys(Keys.ENTER)
        time.sleep(1)

        image_url = selected_products.get("images", "")
        parsed_url = urlparse(image_url)
        ext = os.path.splitext(parsed_url.path)[-1].lower()

        # Force-safe extension
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = ".jpg"

        # Download image content
        response = requests.get(image_url)
        image_data = response.content

        # Convert webp to jpg if needed
        if ext == ".webp":
            with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as temp_webp:
                temp_webp.write(image_data)
                temp_webp_path = temp_webp.name

            # Open and convert to JPG
            with Image.open(temp_webp_path) as im:
                rgb_im = im.convert("RGB")
                fd, temp_image_path = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                rgb_im.save(temp_image_path, "JPEG")

            os.remove(temp_webp_path)  # Clean up .webp file

        else:
            # Save original image if not webp
            fd, temp_image_path = tempfile.mkstemp(suffix=ext)
            os.close(fd)
            with open(temp_image_path, "wb") as f:
                f.write(image_data)

        # Upload the image
        file_input = driver.find_element(
            By.XPATH,
            "(//input[@class='js-file-upload-helper'])[2]",
        )
        file_input.send_keys(temp_image_path)
        print("Image Submitted")
        time.sleep(3)

        image_credit = driver.find_element(
            By.XPATH,
            "//span[@data-placeholder='Who created or owns this image?']",
        )
        image_credit.click()
        time.sleep(1)
        image_credit = driver.find_element(
            By.XPATH,
            "//textarea[@placeholder='Who created or owns this image?']",
        )
        image_credit.click()
        image_credit.send_keys("Bella Hararo")

        image_via = driver.find_element(
            By.XPATH,
            "//span[@data-placeholder='Where did you find it (URL)?']",
        )
        image_via.click()
        time.sleep(1)
        image_via = driver.find_element(
            By.XPATH,
            "//textarea[@placeholder='Where did you find it (URL)?']",
        )
        image_via.click()
        image_via.send_keys("https://bellahararo.com")

        # Upload the image
        file_input_thum = driver.find_element(
            By.XPATH,
            "(//input[@class='js-file-upload-helper'])[4]",
        )
        file_input_thum.send_keys(temp_image_path)
        print("Image Submitted")
        time.sleep(5)

        thum_image_alt = wait.until(
            EC.presence_of_element_located((By.ID, "alt_text_thumbnail_input"))
        )
        thum_image_alt.click()
        alt_tag = selected_products.get("title", "")
        thum_image_alt.send_keys(alt_tag)
        time.sleep(1)
        save = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='js-save button']")
            )
        )
        save.click()
        time.sleep(1)

        post_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@id='quickpost-create-super']")
            )
        )
        post_button.click()
        time.sleep(1)
        print("Post button click")

        print("post button CLicked")
        # Delete temp image
        # Try to delete the file safely with retries
        for _ in range(5):
            try:
                os.remove(temp_image_path)
                print("Temp image deleted.")
                break
            except PermissionError:
                print("Image still in use. Retrying...")
                time.sleep(1)

        time.sleep(5)

    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_products.get('name')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
