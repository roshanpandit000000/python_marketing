import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
import os
import random
from difflib import SequenceMatcher
from urllib.parse import quote_plus


def is_similar(a, b, threshold=0.3):
    similarity = SequenceMatcher(None, a.lower(), b.lower()).ratio()
    # print(f"Similarity between:\n  A: '{a}'\n  B: '{b}'\n  ➤ Score: {similarity:.2f}")
    return similarity >= threshold


def word_overlap_ratio(a, b, threshold=0.3):
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    overlap = set_a & set_b
    ratio = len(overlap) / len(set_a) if set_a else 0
    # print(f"Word Overlap: {overlap} ➤ Ratio: {ratio:.2f}")
    return ratio >= threshold


def image_link(driver, title_text):
    encoded_query = quote_plus(title_text)
    search_url = f"https://www.pinterest.com/search/pins/?q={encoded_query}"
    driver.get(search_url)

    assert "Pinterest" in driver.title

    found_match = False
    scroll_attempts = 0
    max_scrolls = 10

    while scroll_attempts < max_scrolls:
        print(f"\nScroll attempt {scroll_attempts + 1}...")

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@role='listitem']")
                )
            )
            print("List items loaded successfully.")
        except:
            print("Timed out waiting for list items to load.")
            driver.quit()
            exit()

        list_items = driver.find_elements(By.XPATH, "//div[@role='listitem']")
        # print(f"Found {len(list_items)} list items.")

        for item in list_items:
            try:
                img = item.find_element(By.TAG_NAME, "img")
                alt_text = img.get_attribute("alt")

                if alt_text and (
                    is_similar(title_text, alt_text)
                    or word_overlap_ratio(title_text, alt_text)
                ):

                    srcset = img.get_attribute("srcset")
                    if srcset:
                        srcset_urls = srcset.split(", ")
                        original_url = None
                        for url in srcset_urls:
                            if "originals" in url:
                                original_url = url.split(" ")[0]
                                return original_url
                                # break
                    print(f"Matched ALT: {alt_text}")
                    print(f"Image SRC: {original_url}")
                    found_match = True
                    # break  # Stop after first match
            except:
                continue  # Skip any listitem that doesn't have an image

        if not found_match:
            print("❌ No match found this round. Scrolling for more...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_attempts += 1
        else:
            print("✅ Match found. Stopping further search.")
            # break

        # Scroll to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        scroll_attempts += 1

    if not found_match:
        print("😢 No matching images found after scrolling.")
        return None
    # assert "No results found." not in driver.page_source
    # driver.quit()


# Attach to running browser session
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

skip_number = int(input("Enter number of posts to skip: "))

# Load titles from Excel
df = pd.read_excel(
    r"C:\Users\PcHelps\Documents\Python\GPT_article_scraper\Article_Sheet.xlsx"
)  # Replace with actual path

df.columns = df.columns.str.strip()
try:
    url = "https://chat.openai.com/"
    driver.get(url)
    time.sleep(random.uniform(2.5, 4.5))  # Wait for initial content to load
    print("open chat successfull")

    for index, row in df.iterrows():
        if index < skip_number:
            continue
        sheet_title = row["Title"]
        links = [
            str(row[f"Link_0{i}"]) for i in range(1, 7) if pd.notna(row[f"Link_0{i}"])
        ]

        # Join links as a string
        link_text = " ".join(links)

        input_box = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='prompt-textarea']",
                )
            )
        )
        input_box.click()
        # time.sleep(4)
        time.sleep(random.uniform(1.5, 2.5))
        print("Input Click Successfull")

        input_box.send_keys(
            f"Write an professional article about: `{sheet_title}` for backlinking purpose. "
            f"Make sure to include these links in the article: {link_text}."
        )
        time.sleep(random.uniform(1.5, 3.5))
        input_box.send_keys(Keys.RETURN)
        print("✅ Title extracted and sent to ChatGPT! Browser remains open.")
        # Wait for the "Submitting..." message to appear
        time.sleep(random.uniform(1.5, 3.3))
        xpath_status = "//button[@data-testid='composer-speech-button']"
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, xpath_status))
        )
        print("✅ Submit Article Successful, proceeding...")
        time.sleep(random.uniform(1.8, 2.4))
        # Scrap HTML from prosemirror editor container
        response_box = None  # Initialize
        response_html = ""
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, '_main_5jn6z_1') and contains(@class, 'markdown') and contains(@class, 'ProseMirror')]",
                    )
                )
            )
            response_boxes = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, '_main_5jn6z_1') and contains(@class, 'markdown') and contains(@class, 'ProseMirror')]",
            )
            print("✅ ProseMirror response boxes found.")
        except TimeoutException:
            print("⚠️ ProseMirror not found in 2 seconds. Trying fallback selector...")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-message-author-role='assistant']")
                )
            )
            time.sleep(random.uniform(0.8, 1.4))  # Small delay
            response_boxes = driver.find_elements(
                By.XPATH, "//div[@data-message-author-role='assistant']"
            )
            print("✅ Fallback assistant response boxes found.")
            time.sleep(
                random.uniform(0.8, 1.4)
            )  # Small delay to avoid overloading the browser

        # Always get the last element from whichever selector worked
        if response_boxes:
            response_box = response_boxes[-1]

            driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                response_box,
            )

            response_html = response_box.get_attribute("outerHTML")
            print("📝 Last response HTML scraped.")
        else:
            raise Exception("❌ No response boxes found from either selector.")

        print("📝 ChatGPT Response HTML:")
        soup = BeautifulSoup(response_html, "html.parser")

        # 1. Remove the first <p> tag
        first_p = soup.find("p")
        if first_p:
            first_p.decompose()

        # 2. Remove the last <p> tag
        all_p = soup.find_all("p")
        if all_p:
            all_p[-1].decompose()

        # Step 5: Extract structured data
        # 3. Extract <h1> as title
        h1 = soup.find("h1")
        title = str(h1.get_text(strip=True)) if h1 else str(sheet_title)

        # 4. Find first <p> after <h1> for subtitle
        subtitle = ""
        if h1:
            next_sibling = h1.find_next_sibling()
            found = False
            while next_sibling:
                if next_sibling.name == "p":
                    subtitle = next_sibling.get_text(strip=True)
                    found = True
                    break
                next_sibling = next_sibling.find_next_sibling()
            if not found:
                # fallback: get the second <p> tag from the entire document
                p_tags = soup.find_all("p")
                if len(p_tags) >= 3:
                    subtitle = p_tags[1].get_text(strip=True)
        # open a new tab and find image on pinterest
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        print("New tab opened for Pinterest search.")
        original_url = image_link(driver, title)
        time.sleep(1)
        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        article_data = {
            "title": title,
            "subtitle": subtitle,
            "image": original_url,
            "description": str(soup),
            "slug": links[0] if links else "",
        }
        # Wait for response to generate
        time.sleep(random.uniform(0.8, 2.4))
        # Save HTML response to a file
        # Step 6: Save to JSON file
        json_path = r"C:\Users\PcHelps\Documents\Python\GPT_article_scraper\chatgpt_response.json"
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # === STEP 4: Append and save ===
        data.append(article_data)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("✅ Article appended to chatgpt_response.json.")

        time.sleep(1)
        print("click Submit Button")

        if index % random.randint(5, 9) == 0:
            pause_time = random.uniform(10, 20)
            print(f"😴 Taking a human-like break for {pause_time:.1f} seconds...")
            time.sleep(pause_time)
except Exception as e:
    print(f"Error submitting article: {e}\n")
