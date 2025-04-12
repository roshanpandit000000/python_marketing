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


for index, selected_article in enumerate(articles, start=1):
    total = len(articles)
    print(
        f"\n=== Submitting Article {index} of {total}: {selected_article.get('title', 'Untitled')} ==="
    )

    article_data = {
        "title": selected_article.get("title", ""),
        "mainDescription": selected_article.get("mainDescription", ""),
        "image_url": selected_article.get("images", ""),
        "subtitle": selected_article.get("shortDescription", ""),
        "link": selected_article.get("slug", ""),
    }

    try:
        driver.get("https://www.tumblr.com/")
        time.sleep(5)  # Wait for initial content to load

        create = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@aria-label='Create a post']")
            )
        )
        create.click()
        time.sleep(1)
        print(f"Click 'Create' Button")
        time.sleep(1)

        new_link = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/new/link']"))
        )
        new_link.click()
        time.sleep(1)
        print(f"Click 'new Link' Button")
        time.sleep(1)

        link_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Type or paste link']")
            )
        )
        time.sleep(1)
        print(f"Link input field found")
        link = "https://bellahararo.com/articles/" + selected_article.get("slug", "")
        print(f"Link: {link}")
        time.sleep(1)
        link_input.send_keys(link)
        time.sleep(1)

        insert_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Insert']"))
        )
        time.sleep(1)
        print(f"Insert button found")
        insert_button.click()
        time.sleep(1)

        post_card = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@data-title='Link card'])[2]")
            )
        )
        time.sleep(2)

        if post_card.is_displayed():
            print("Card is displayed")
            time.sleep(1)

            # Re-fetch the <select> element after the DOM update
            tag_editor = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//textarea[@aria-label='Tags editor']")
                )
            )
            tag_editor.click()
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
                "WigLife",
                "BundleDeals",
                "BlackGirlMagic",
                "CurlyHair",
                "StraightHair",
                "BlondeHair",
                "ProtectiveStyles",
                "NaturalHairCommunity",
                "Wigslayed",
                "SelfCare",
                "GlamLife",
                "SlayAllDay",
                "MakeupAndHair",
                "GlowUp",
                "BeforeAndAfter",
                "BeautyBlogger",
            ]

            for tag in tags:
                tag_editor.send_keys(tag)
                tag_editor.send_keys(Keys.RETURN)
                time.sleep(1)
            time.sleep(2)
            print("Tags added successfully")
        else:
            print("Tags is not displayed")
        print("Tags Done")
        time.sleep(2)

        post_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button//span[text()='Post now']")
            )
        )
        time.sleep(1)
        print(f"Post button found")
        post_button.click()
        time.sleep(5)

        print("All inputs filled successfully!")
    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_article.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
