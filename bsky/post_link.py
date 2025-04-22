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
import pyperclip


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

    try:
        driver.get("https://bsky.app/")
        time.sleep(3)  # Wait for initial content to load

        create = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//button[@aria-label='New post' and @data-testid='composeFAB'])[1]",
                )
            )
        )
        create.click()
        time.sleep(1)
        print(f"Click 'Create' Button")

        link_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@aria-label='Rich-Text Editor'])")
            )
        )
        time.sleep(1)
        print(f"Link input field found")
        link = "https://bellahararo.com/articles/" + selected_article.get("slug", "")
        print(f"Link: {link}")
        time.sleep(1)
        pyperclip.copy(link)
        link_input.send_keys(Keys.CONTROL + "v")
        time.sleep(1)
        # link_input.click()
        link_input.send_keys(Keys.ENTER, Keys.ENTER)

        tags = "#hair #hairextenion #RIP #PopeFrancis #Celtics #Protests #PeteHegseth #UkrainianView #Books #Art #Comics #Animals #Photography #Tech #Science #Politics #Writers #Weft #WeftHairExtensions"
        
        pyperclip.copy(tags)
        link_input.send_keys(Keys.CONTROL + "v")
        time.sleep(1)
        try:
            xpath_status = f"//a[@href='{link}']"
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.XPATH, xpath_status))
            )
            print("Submit Article Successful, proceeding...")

            post_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//button[@aria-label='Publish post'])")
                )
            )
            time.sleep(1)
            print(f"Post button found")
            post_button.click()

            xpath_post_done = "(//div[text()='Your post has been published'])"
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.XPATH, xpath_post_done))
            )
            print("post Submited Successfully. Proceeding Next Post....")

        except Exception as e:
            print("No 'Submitting...' message or URL didn't change — skipping wait.")

        # time.sleep()

        print("All inputs filled successfully!")
    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_article.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
