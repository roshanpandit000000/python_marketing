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


# API Endpoint for Articles
API_URL = "https://bellahararo.com/api/products"
response = requests.get(API_URL)
data = response.json()
products = data.get("products", [])

# Exit if no article
SKIP_COUNT = int(input("Enter number of posts to skip: "))
products = products[SKIP_COUNT:]


def extract_text_with_links(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove all tags except <br>
    for tag in soup.find_all():
        if tag.name != "br":
            tag.unwrap()  # removes the tag but keeps the text

    for br in soup.find_all("br"):
        br.replace_with("\n")
    # Convert to string, keeping <br> tags in place
    final_text = str(soup)

    return final_text


for index, selected_product in enumerate(products, start=1):
    total = len(products)
    print(
        f"\n=== Submitting Article {index} of {total}: {selected_product.get('title', 'Untitled')} ==="
    )

    article_data = {
        "title": selected_product.get("title", ""),
        "mainDescription": selected_product.get("mainDescription", ""),
        "image_url": selected_product.get("images", ""),
        "subtitle": selected_product.get("shortDescription", ""),
        "link": selected_product.get("slug", ""),
    }

    html_description = selected_product.get("mainDescription", "")
    plain_text_description = extract_text_with_links(html_description)

    time.sleep(4)
    print(plain_text_description)
    time.sleep(4)
    exit()


time.sleep(5)  # Wait for the page to load before closing the driver
