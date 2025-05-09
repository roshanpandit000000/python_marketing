import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select
import json
import random
import pyautogui
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# API Endpoint for Articles
json_path = (
    r"C:\Users\PcHelps\Documents\Python\GPT_article_scraper\chatgpt_response.json"
)

# Load data from the JSON file
with open(json_path, "r", encoding="utf-8") as f:
    articles = json.load(f)


SKIP_COUNT = int(input("Enter number of posts to skip: "))
MAX_POSTS = int(input("Enter the number of posts to submit: "))
articles = articles[SKIP_COUNT : SKIP_COUNT + MAX_POSTS]

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
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
    """
    },
)
# wait = WebDriverWait(driver, 15)

Categorys = [
    "Clip-In Extensions",
    "Hair Bundles",
    "Hair Care for Extensions",
    "Hair Extension",
    "Hair Toppers",
    "Lace Front Wigs",
    "Ponytail Extensions",
    "Pre-Bonded Extensions",
    "Sew-In Weaves",
    "Tape-In Extensions",
    "Wigs",
]

# === Step 1: Ask for category selection ===
print("\nAvailable Categories:")
for i, cat in enumerate(Categorys, start=1):
    print(f"{i}. {cat}")

while True:
    try:
        selected_index = int(input("\nEnter the number of the category to use: "))
        if 1 <= selected_index <= len(Categorys):
            blog_category = Categorys[selected_index - 1]
            print(f"\n✅ Selected Category: {blog_category}")
            break
        else:
            print("❌ Invalid number. Try again.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Exit if no articles
if not articles:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()


try:
    for index, selected_articles in enumerate(articles, start=1):

        total = len(articles)
        print(
            f"\n=== Submitting post {index} of {total}: {selected_articles.get('title', 'Untitled')} ==="
        )
        try:
            slug = "https://bellahararo.com/"
            title = selected_articles.get("title", "")
            subtitle = selected_articles.get("subtitle", "")
            image_url = selected_articles.get("image", "")
            description = selected_articles.get("description", "")
            link = f"[{title}]({slug})"
            # print(f"Title: {title}")
            # print(f"Subtitle: {subtitle}")
            time.sleep(random.uniform(2.5, 4.5))

            try:
                driver.get("https://bellahararo.infy.uk/wp-admin/post-new.php")
                time.sleep(random.uniform(1.5, 3.5))
                # Type each image path and press 'enter'
                wait.until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.NAME, "editor-canvas")
                    )
                )
                print("✅ Switched to iframe")
                title_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//h1[@aria-label='Add title']",
                        )
                    )
                )
                title_input.click()
                title_input.clear()
                # pyperclip.copy(title)
                title_input.send_keys(title)
                print("✅ Title input filled")
                time.sleep(random.uniform(0.5, 2.5))

                plus_button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@aria-label='Add block']",
                        )
                    )
                )
                plus_button.click()
                print("✅ Plus button clicked")
                driver.switch_to.default_content()
                plus_button_search = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//input[@placeholder='Search']",
                        )
                    )
                )
                plus_button_search.click()
                plus_button_search.clear()
                plus_button_search.send_keys("html")
                html_button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@type='button']//span[text()='Custom HTML']",
                        )
                    )
                )
                html_button.click()
                print("✅ URL input filled")
                time.sleep(random.uniform(0.5, 2.5))
                wait.until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.NAME, "editor-canvas")
                    )
                )
                print("✅ Switched to iframe")
                html_input = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "textarea.block-editor-plain-text")
                    )
                )
                pyperclip.copy(description)

                html_input.click()

                html_input.send_keys(Keys.CONTROL, "v")
                # time.sleep(1)
                print("✅ Html input send")
                time.sleep(random.uniform(0.5, 2.5))
                driver.switch_to.default_content()

                time.sleep(random.uniform(0.5, 2.5))
                post_preview = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[text()='Preview']",
                        )
                    )
                )
                post_preview.click()
                post_tab = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@data-tab-id='edit-post/document']",
                        )
                    )
                )
                post_tab.click()
                print("✅ Body input filled")
                time.sleep(random.uniform(0.5, 2.5))

                # Select the language from the dropdown
                feture_image = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[text()='Set featured image']")
                    )
                )
                feture_image.click()

                upload_files = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@id='menu-item-upload']")
                    )
                )
                upload_files.click()
                upload_files_url = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "(//button[text()='Select Files'])")
                    )
                )
                upload_files_url.click()
                time.sleep(3)
                # open file diloge
                pyautogui.write(image_url)
                time.sleep(1)  # Give dialog time to fully appear
                pyautogui.press("enter")
                time.sleep(1)
                print("✅ URL input filled")
                time.sleep(random.uniform(0.5, 2.5))
                image_upload_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "(//button[text()='Set featured image'])[2]",
                        )
                    )
                )
                image_upload_button.click()
                print("✅ Create post button clicked")
                time.sleep(random.uniform(0.5, 2.5))
                side_bar = wait.until(
                    EC.presence_of_element_located(
                        (By.ID, "tabs-0-edit-post/document-view")
                    )
                )
                category_input = side_bar.find_element(
                    By.XPATH, f"//label[text()='{blog_category}']"
                )
                print("✅ Alt input found")

                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                    category_input,
                )
                category_input.click()
                tag_input = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "(//input[@role='combobox'])",
                        )
                    )
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                    tag_input,
                )
                tag_input.click()
                tag_input.send_keys(
                    "hair, hair extension, hair care, hair product, hair color, hair style,"
                )
                print("✅ Tag input filled")
                time.sleep(random.uniform(0.5, 2.5))
                publish_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "(//button[text()='Publish'])[1]",
                        )
                    )
                )
                publish_button.click()
                time.sleep(random.uniform(0.5, 2.5))
                publish_button_again = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "(//button[text()='Publish'])[2]",
                        )
                    )
                )
                publish_button_again.click()

                print("✅ Publish button clicked")
                # Wait for the "Submitting..." message to appear

                # Wait for the "Submitting..." message to appear

                xpath_status = "(//button[text()='Save'])"
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, xpath_status))
                )
                print("✅ Submit Article Successful, proceeding...")
                time.sleep(random.uniform(0.5, 2.5))
                if index % random.randint(8, 15) == 0:
                    pause_time = random.uniform(20, 40)
                    print(
                        f"😴 Taking a human-like break for {pause_time:.1f} seconds..."
                    )
                    time.sleep(pause_time)
            except Exception as e:
                print(
                    "No 'Submitting...' message or URL didn't change — skipping wait."
                )
        except Exception as e:
            print(
                f"Error submitting article {index} ({selected_articles.get('title')}): {e}\n"
            )
        continue

except Exception as e:
    print(f"General error: {e}")

time.sleep(5)  # Wait for the page to load before closing the driver
driver.quit()
