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

# API Endpoint for Articles
json_path = (
    r"C:\Users\PcHelps\Documents\Python\GPT_article_scraper\chatgpt_response.json"
)

# Load data from the JSON file
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data if isinstance(data, list) else data.get("articles", [])


SKIP_COUNT = int(input("Enter number of posts to skip: "))
MAX_POSTS = int(input("Enter the number of posts to submit: "))
articles = articles[SKIP_COUNT : SKIP_COUNT + MAX_POSTS]

chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
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
wait = WebDriverWait(driver, 15)


# Exit if no articles
if not articles:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()


def extract_text_with_links(html):

    soup = BeautifulSoup(html, "html.parser")

    # Step 1: Replace <a> with "text (link)"
    for a in soup.find_all("a"):
        href = a.get("href")
        text = a.get_text(strip=True)
        if href:
            a.replace_with(f"[{text}]({href})")
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
            time.sleep(random.uniform(2.5, 4.5))

            try:
                driver.get("https://lemm.ee/create_post?communityId=20926")
                time.sleep(2)
                # Type each image path and press 'enter'
                title_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//textarea[@id='post-title']",
                        )
                    )
                )
                title_input.click()
                title_input.clear()
                title_input.send_keys(title)
                print("✅ Title input filled")
                time.sleep(random.uniform(0.5, 2.5))

                url_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//input[@id='post-url']",
                        )
                    )
                )
                url_input.click()
                url_input.clear()
                url_input.send_keys(slug)
                print("✅ URL input filled")
                time.sleep(random.uniform(0.5, 2.5))
                thumbnail_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//input[@id='post-custom-thumbnail']",
                        )
                    )
                )
                thumbnail_input.click()
                thumbnail_input.send_keys(image_url)
                print("✅ Thumbnail input clicked")
                time.sleep(random.uniform(0.5, 2.5))
                body_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "(//textarea[@required])[2]",
                        )
                    )
                )
                body_input.click()
                body_input.clear()
                formatted_title = f"**{title}**"
                plain_text_description = extract_text_with_links(description)
                main_text_input = (
                    formatted_title + "\n\n" + plain_text_description + "\n\n" + link
                )

                body_input.send_keys(main_text_input)
                print("✅ Body input filled")
                time.sleep(1)

                # Select the language from the dropdown
                select_element = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "(//select[@aria-label='Select language'])")
                    )
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                    select_element,
                )
                time.sleep(random.uniform(0.5, 2.5))
                select_option = Select(select_element)
                select_option.select_by_value("37")
                print(f"✅ Select 'Option' Input")
                time.sleep(random.uniform(0.5, 2.5))
                create_post_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[text()='Create']",
                        )
                    )
                )
                create_post_button.click()
                print("✅ Create post button clicked")
                time.sleep(random.uniform(0.5, 2.5))

                # Wait for the "Submitting..." message to appear
                xpath_status = "(//textarea[@placeholder='Type here to comment...'])"
                WebDriverWait(driver, 20).until(
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
