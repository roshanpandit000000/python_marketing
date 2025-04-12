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
    print("No Product found from the API. Exiting.")
    driver.quit()
    exit()

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

    safe_text = "".join(c for c in final_text if ord(c) <= 0xFFFF)

    return safe_text


for index, selected_product in enumerate(products, start=1):
    total = len(products)
    print(
        f"\n=== Submitting Product {index} of {total}: {selected_product.get('name', 'Untitled')} ==="
    )

    article_data = {
        "name": selected_product.get("name", ""),
        "mainDescription": selected_product.get("mainDescription", ""),
        "image_url": selected_product.get("images", ""),
        "subtitle": selected_product.get("shortDescription", ""),
        "link": selected_product.get("slug", ""),
    }

    try:
        driver.get("https://www.tumblr.com/new/link/")
        time.sleep(5)  # Wait for initial content to load

        # create = wait.until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, "//a[@aria-label='Create a post']")
        #     )
        # )
        # time.sleep(1)
        # create.click()
        # print(f"Click 'Create' Button")
        # time.sleep(1)

        # new_link = wait.until(
        #     EC.presence_of_element_located((By.XPATH, "//a[@href='/new/link']"))
        # )
        # time.sleep(1)
        # print(f"New Link button found")
        # new_link.click()
        # time.sleep(1)
        # print(f"Click 'new Link' Button")
        # time.sleep(1)

        link_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Type or paste link']")
            )
        )
        time.sleep(1)
        print(f"Link input field found")
        link_input.click()
        link = "https://bellahararo.com/shop/" + selected_product.get("slug", "")
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
        time.sleep(5)
        print(f"Insert button clicked")
        post_card = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@data-title='Link card'])[2]")
            )
        )
        time.sleep(1)

        if post_card.is_displayed():
            print("Card is displayed")
            time.sleep(1)
            textarea = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[@aria-label='Add default block']")
                )
            )
            time.sleep(1)
            print(f"Textarea found")
            textarea.click()
            time.sleep(1)
            print(f"Textarea clicked")
            time.sleep(1)
            text_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//p[@role='document']"))
            )
            time.sleep(1)
            print(f"Text input field found")
            text_input.click()

            html_description = selected_product.get("mainDescription", "")
            plain_text_description = extract_text_with_links(html_description)

            time.sleep(1)
            text_input.send_keys(plain_text_description)
            time.sleep(3)
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
            f"Error submitting article {index} ({selected_product.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
