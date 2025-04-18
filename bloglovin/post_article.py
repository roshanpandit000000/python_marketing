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
        driver.get("https://www.bloglovin.com/new-post")
        time.sleep(2)  # Wait for initial content to load

        title = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//div[@aria-describedby])[1]"))
        )
        title.click()
        time.sleep(1)
        pyperclip.copy(selected_products.get("title", ""))
        title.send_keys(Keys.CONTROL + "v")
        print(f"Send 'Title' Input")
        time.sleep(1)

        subtitle = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//div[@aria-describedby])[1]"))
        )
        subtitle.click()
        time.sleep(1)
        pyperclip.copy(selected_products.get("shortDescription", ""))
        subtitle.send_keys(Keys.CONTROL + "v")
        print(f"Send 'Subtitle' Input")
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
            "(//input[@class='post-editor-uploader-input js-file-upload-input'])",
        )
        file_input.send_keys(temp_image_path)
        print("Image Submitted")
        time.sleep(3)

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

        description = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr'])[3]",
                )
            )
        )
        description.click()
        time.sleep(1)
        html_description = selected_products.get("mainDescription", "")
        plain_text_description = extract_text_with_links(html_description)
        # print(plain_text_description)
        time.sleep(1)
        pyperclip.copy(plain_text_description)
        description.send_keys(Keys.CONTROL + "v")
        print("Add Description Done")
        description.send_keys(Keys.ENTER)
        time.sleep(1)

        post_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//span[text()='Post'])[1]"))
        )
        post_button.click()
        time.sleep(1)
        print("Post button click")

        try:
            print("post_button")
            time.sleep(1)

            # Re-fetch the <select> element after the DOM update
            tags_input = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//input[@value='Add tags...'])")
                )
            )
            tags_input.click()
            time.sleep(1)
            print(f"Clicked 'Tag Editor' Div")
            tags = [
                "HairExtensions",
                "HairGoals",
                "HairInspo",
                "HairTransformation",
                "BeautyTips",
                "HairCare",
                "LongHairDontCare",
                "HairRoutine",
                "ClipInExtensions",
                "VirginHair",
                "RemyHair",
                "HumanHairExtensions",
                "SeamlessExtensions",
                "TapeInExtensions",
                "BlackGirlMagic",
            ]

            for tag in tags:
                tags_input.send_keys(tag)
                tags_input.send_keys(Keys.RETURN)
                time.sleep(1)
            time.sleep(1)
            print("Tags added successfully")
        except Exception as e:
            print(f"Error adding tags: {e}")
        print("Tags Done")
        time.sleep(1)

        post_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//div[@class='post-editor-dropdown-final-btn btn-filled'])",
                )
            )
        )
        time.sleep(1)
        print(f"Post button found")
        post_button.click()
        print("post button CLicked")

        time.sleep(5)

    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_products.get('name')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
