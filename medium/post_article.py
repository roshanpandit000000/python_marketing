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
import pyautogui
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Set up Chrome options
options = Options()

# Point to your user data directory
options.add_argument(
    r"--user-data-dir=C:\Users\PcHelps\AppData\Local\Google\Chrome\User Data"
)
options.add_argument(
    "--profile-directory=Profile 7"
)  # Or 'Profile 1', 'Profile 2', etc.

# Optional: Keep browser open after script
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(), options=options)
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
MAX_POSTS = int(input("Enter the number of posts to submit: "))
articles = articles[SKIP_COUNT:]


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


for index, selected_article in enumerate(articles, start=1):
    if index > MAX_POSTS:
        print(f"\nReached the limit of {MAX_POSTS} posts. Exiting loop.")
        break
    total = len(articles)
    print(
        f"\n=== Submitting Article {index} of {total}: {selected_article.get('title', 'Untitled')} ==="
    )
    image_url = selected_article.get("images", "Untitled")
    image_path = os.path.abspath("cover_image.jpg")

    with open(image_path, "wb") as f:
        f.write(requests.get(image_url).content)
        print("Image is saveda")

    try:
        driver.get("https://medium.com/new-story")
        time.sleep(3)  # Wait for initial content to load

        title = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h3[@data-testid='editorTitleParagraph']",
                )
            )
        )
        title.click()
        title_text = selected_article.get("title", "Untitled")
        pyperclip.copy(title_text)
        time.sleep(1)
        title.send_keys(Keys.CONTROL + "v")
        print(f"'title' Input Send")
        # title.send_keys(Keys.ENTER)
        time.sleep(3)
        content_input = driver.find_element(
            By.XPATH, "(//p[@data-testid='editorParagraphText'])"
        )
        content_input.click()
        image_plus = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@aria-label='Add an image, video, embed, or new part']",
                )
            )
        )
        image_plus.click()
        image = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@aria-label='Add an image']",
                )
            )
        )
        image.click()
        print(image_path)
        time.sleep(2)
        pyautogui.write(image_path)
        time.sleep(1)  # Give dialog time to fully appear
        pyautogui.press("enter")
        time.sleep(1)
        print("Image Added")
        # image = wait.until(
        #     EC.presence_of_element_located(
        #         (
        #             By.XPATH,
        #             "//img[@class='graf-image']",
        #         )
        #     )
        # )
        # image.click()

        alt = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@data-action='alt']",
                )
            )
        )
        alt.click()
        time.sleep(5)
        alt_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@data-placeholder-text='E.g., An antique typewriter with a blank sheet of paper sits on a wooden desk']",
                )
            )
        )
        alt_input.click()
        alt_input.send_keys(Keys.CONTROL + "v")

        alt_save = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@data-action='overlay-submit']",
                )
            )
        )
        alt_save.click()
        print("click alt save button")
        time.sleep(2)
        content_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "(//p[@data-testid='editorParagraphText'])")
            )
        )
        content_input.click()
        print("content click")
        driver.execute_script(
            """
            if (arguments[0]) {
                arguments[0].innerHTML += arguments[1];
            }
            """,
            content_input,
            selected_article.get("mainDescription", "Untitled"),
        )
        time.sleep(2)
        publish_button = driver.find_element(
            By.XPATH, "//button[@data-action='show-prepublish']"
        )
        publish_button.click()
        try:
            topics = [
                "hair",
                "beauty",
                "fashion",
                "style",
                "makeup",
                "extensions",
                "wigs",
                "salon",
            ]
            max_options = 5  # Max number of topics to add

            for index in range(min(len(topics), max_options)):
                # Re-locate the topic input each time to avoid stale element reference
                topic_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//div[@data-testid='publishTopicsInput']",
                        )
                    )
                )
                topic_input.click()
                time.sleep(1)

                # Send the topic input
                topic_input.send_keys(topics[index])
                time.sleep(1)

                # Select the first available suggestion
                first_suggestion = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "(//li[@data-action='typeahead-populate'])[1]")
                    )
                )
                first_suggestion.click()
                time.sleep(1)

                print(f"✅ Added topic: {topics[index]}")

            # Click the "Publish now" button after selecting topics
            publish_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@data-action='publish']")
                )
            )
            publish_button.click()

            WebDriverWait(driver, 15).until(EC.url_contains("@bellahararo"))
            print("Submit Article Successful, proceeding...")

            time.sleep(3)

            print("✅ Topics added and article published successfully!")

        except Exception as e:
            print(f"❌ Error in adding topics or publishing: {e}")

        # time.sleep()

        print("All inputs filled successfully!")
    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_article.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
