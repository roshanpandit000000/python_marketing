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

html_data = '<p data-start="2801" data-end="3124" class="">At the end of the day, confidence isn’t about perfection—it’s about <em data-start="2869" data-end="2879">presence</em>. It’s about showing up authentically and unapologetically. And when you want a little boost on the outside to match your inner fire,<a href="https://bellahararo.com/" target="_blank" style="color: rgb(60, 120, 216);"> <strong data-start="3013" data-end="3029">Bella Hararo</strong></a> offers luxurious, natural-looking hair extensions that help you feel as bold as you truly are.</p><p data-start="2801" data-end="3124" class=""><br></p>\n<p data-start="3126" data-end="3229" class="">Because when you look in the mirror and <em data-start="3166" data-end="3172">love</em> what you see, you radiate that energy everywhere you go.</p>'

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
    driver.get(
        "https://www.linkedin.com/article/new/?author=urn%3Ali%3Afsd_company%3A102952256"
    )
    time.sleep(4)  # Wait for initial content to load

    description = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
    )
    description.click()
    time.sleep(1)
    plain_text_description = extract_text_with_links(html_data)
    description.send_keys(plain_text_description)
    print("Description Send Success")
    time.sleep(2)

    next_article = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button//span[text()='Next']"))
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
    pyperclip.copy("Top Ways For Women To Boost Their Confidence Today")
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
    print(f"Error submitting article: {e}\n")
