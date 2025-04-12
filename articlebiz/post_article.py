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
API_URL = "https://bellahararo.com/api/article"
response = requests.get(API_URL)
data = response.json()
articles = data.get("articles", [])

# Exit if no articles
if not articles:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()

SKIP_COUNT = int(input("Enter number of posts to skip: "))
articles = articles[SKIP_COUNT:]


EMOJI_PATTERN = re.compile(
    "["
    "\U00010000-\U0010ffff"  # Match characters outside the BMP
    "]+",
    flags=re.UNICODE,
)


def extract_clean_paragraphs(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags (like img, br, script, style)
    for tag in soup(["script", "style", "img", "br"]):
        tag.decompose()

    # Collapse inline tags (strong, span, etc.) by unwrapping them (keep text, remove tag)
    for tag in soup.find_all(["strong", "em", "b", "i", "u", "span"]):
        tag.unwrap()

    # Extract text in block-level tags (p, h1-h6, li, etc.)
    blocks = []
    for tag in soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            text = EMOJI_PATTERN.sub("", text)
            blocks.append(text)

    return "\n\n".join(blocks)  # Two newlines = paragraph spacing


for index, selected_article in enumerate(articles, start=1):
    total = len(articles)
    print(
        f"\n=== Submitting Article {index} of {total}: {selected_article.get('title', 'Untitled')} ==="
    )

    article_data = {
        "title": selected_article.get("title", ""),
        "mainDescription": selected_article.get("mainDescription", ""),
        "image_url": selected_article.get("images", ""),
    }

    try:
        driver.get("https://articlebiz.com/submitArticle")
        time.sleep(5)  # Wait for initial content to load

        author_name = wait.until(EC.presence_of_element_located((By.ID, "authorName")))
        author_name.click()
        time.sleep(1)
        author_name.send_keys("Bella Hararo")
        print(f"Send 'Author Name' Input")
        time.sleep(1)

        email = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email.click()
        time.sleep(1)
        email.send_keys("bellbellahararo.hairextension@gmail.com")
        print(f"Send 'Email' Input")
        time.sleep(1)

        title = wait.until(EC.presence_of_element_located((By.ID, "title")))
        title.click()
        time.sleep(1)
        title.send_keys(article_data["title"])
        print(f"Send 'Title' Input")
        time.sleep(1)

        select_element = wait.until(
            EC.presence_of_element_located((By.ID, "categoryId"))
        )
        select_option = Select(select_element)
        select_option.select_by_value("93")
        print(f"Select 'Option' Input")
        time.sleep(1)

        html_description = selected_article.get("mainDescription", "")
        plain_text_description = extract_clean_paragraphs(html_description)
        time.sleep(3)
        body = wait.until(EC.presence_of_element_located((By.ID, "body")))
        body.click()
        time.sleep(1)
        body.send_keys(plain_text_description)
        print(f"Send 'Body' Input")
        time.sleep(1)

        biography = wait.until(EC.presence_of_element_located((By.ID, "biography")))
        biography.click()
        time.sleep(1)
        biography.send_keys(
            "we are a hair extension company that specializes in hair extensions. Our products are made from 100% Remy human hair, https://bellahararo.com/collections ensuring a natural look and feel. We are committed to providing high-quality hair extensions that are easy to apply and maintain. https://bellahararo.com/"
        )
        print(f"Send 'biography' Input")
        time.sleep(1)

        label_text = driver.find_element(By.XPATH, "//label[@for='mathcaptcha']").text

        numbers = re.findall(r"\d+", label_text)
        if "+" in label_text:
            result = int(numbers[0]) + int(numbers[1])
        elif "-" in label_text:
            result = int(numbers[0]) - int(numbers[1])
        elif "*" in label_text or "x" in label_text.lower():
            result = int(numbers[0]) * int(numbers[1])
        elif "/" in label_text:
            result = int(numbers[0]) / int(numbers[1])
        else:
            raise Exception("Unknown operator in CAPTCHA")

        # Fill in the answer
        input_field = wait.until(EC.presence_of_element_located((By.ID, "mathcaptcha")))
        input_field.click()

        time.sleep(1)
        input_field.send_keys(str(result))
        print(f"Send 'mathcaptcha' Input")
        time.sleep(1)

        label = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='acceptTos']"))
        )
        label.click()
        print("Clicked 'acceptTos' label to check the box")

        submit = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        submit.click()
        time.sleep(1)
        print(f"CLick on Submit Button")
        time.sleep(1)

        wait.until(EC.url_contains("/submitArticle/review"))
        print("Redirected to review page")

        current_url = driver.current_url
        if "/submitArticle/review" in current_url:
            print("Confirmed review page")
        else:
            print("Still on first page or something went wrong")

        # 3. Wait for the second submit button to appear, then click
        second_submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        second_submit.click()
        print("Clicked second submit button")

        print("All inputs filled successfully!")
    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_article.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
