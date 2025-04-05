from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import requests
import json
import re
import pyperclip

# Set up Chrome to use an existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=chrome_options)  # Attach to existing browser

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


def extract_text_with_links(html):
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href")
        text = a.get_text()
        if href:
            a.replace_with(f"{text} ({href})")  # Keep link in format: Text (URL)

    return soup.get_text(separator="\n")  # Preserve line breaks


# Example: loop through each article
for selected_article in articles:
    article_data = {
        "title": selected_article.get("title", ""),
        "mainDescription": selected_article.get("mainDescription", ""),
        "image_url": selected_article.get("images", ""),
    }

    # Open Quora (or category-specific URL if available)
    driver.get("https://www.quora.com/")
    time.sleep(6)  # Wait for page to load

    try:
        wait = WebDriverWait(driver, 10)
        click_add = driver.find_element(
            By.XPATH,
            "//button[@aria-label='Add question' and @aria-haspopup='dialog']",
        )
        click_add.click()
        print(f"Clicked 'Add question' button")
        time.sleep(3)
    except Exception as e:
        print(f"Error clicking button for: {e}")

    # Select first Article
    try:
        wait = WebDriverWait(driver, 10)
        creat_post_button = driver.find_element(
            By.XPATH,
            "//div[text()='Create Post']",
        )
        creat_post_button.click()
        print("Create Post clicked")
        time.sleep(2)
    except Exception as e:
        print(f"Click Create Post error: {e}")

    try:
        # Wait for Quora's editable doc container
        wait = WebDriverWait(driver, 10)
        doc_div = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-kind='doc' and @contenteditable='true']")
            )
        )

        doc_div.send_keys(Keys.CONTROL + "a")  # Select all text in the doc
        time.sleep(2)
        doc_div.send_keys(Keys.DELETE)  # Delete selected text
        time.sleep(2)

        html_description = selected_article.get("mainDescription", "")
        plain_text_description = extract_text_with_links(html_description)

        pyperclip.copy(article_data["image_url"] + "\n\n" + plain_text_description)
        time.sleep(2)
        doc_div.click()  # Click to focus on the doc
        time.sleep(2)
        doc_div.send_keys(Keys.CONTROL + "v")  # Paste the article content
        time.sleep(4)

        print("✅ Rich article content inserted!")

        try:
            post = driver.find_element(
                By.XPATH, "(//button[.//div[text()='Post']])[1]"
            )  # Modify XPath if needed
            original_window = driver.current_window_handle
            before_tabs = driver.window_handles

            post.click()
            print("Post button clicked")
            time.sleep(2)

            # Check for new tab
            after_tabs = driver.window_handles
            if len(after_tabs) > len(before_tabs):
                new_tab = [tab for tab in after_tabs if tab != original_window][0]
                driver.switch_to.window(new_tab)
                print("New tab opened for posted article. Closing it...")
                time.sleep(2)
                driver.close()
                driver.switch_to.window(original_window)
                print("Switched back to original Quora tab.")
        except:
            print("No Post button clicked.")

        print("✅ Article posted successfully!")
    except Exception as e:
        print(f"❌ Error posting article: {e}")


time.sleep(8)  # Pause if needed before next article
