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

# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
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

# Load titles from Excel
df = pd.read_excel(
    r"C:\Users\PcHelps\Documents\Python\GPT_article_scraper\article_title.xlsx"
)  # Replace with actual path
titles = df.iloc[:, 0].dropna().tolist()  # Get first column as a list

try:
    url = "https://chat.openai.com/"
    driver.get(url)
    time.sleep(random.uniform(2.5, 4.5))  # Wait for initial content to load
    print("open chat successfull")

    for index, title in enumerate(titles):
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
            f"Write an professional article about: `{title}` for backlinking purpose. "
            "Make sure to include a `https://bellahararo.com/shop/`, `https://bellahararo.com/collections`, `https://bellahararo.com/` link in the article. "
        )
        time.sleep(random.uniform(1.5, 3.5))
        input_box.send_keys(Keys.RETURN)
        print("✅ Title extracted and sent to ChatGPT! Browser remains open.")
        # Wait for the "Submitting..." message to appear
        time.sleep(random.uniform(0.5, 2.3))
        xpath_status = "//button[@data-testid='composer-speech-button']"
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, xpath_status))
        )
        print("✅ Submit Article Successful, proceeding...")
        time.sleep(random.uniform(0.8, 1.4))
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

        # 4. Add CSS styling for <a> tags
        style_tag = soup.new_tag("style")
        style_tag.string = """
        a {
            color: blue !important;
            text-decoration: underline !important;
            font-weight: bold !important;
        }
        """
        # Insert the style tag at the top of the document
        if soup.body:
            soup.body.insert(0, style_tag)
        else:
            # fallback for fragments
            soup.insert(0, style_tag)

        # Step 5: Extract structured data
        # 3. Extract <h1> as title
        h1 = soup.find("h1")
        title = h1.get_text(strip=True) if h1 else ""

        # 4. Find first <p> after <h1> for subtitle
        subtitle = ""
        if h1:
            next_sibling = h1.find_next_sibling()
            while next_sibling:
                if next_sibling.name == "p":
                    subtitle = next_sibling.get_text(strip=True)
                    break
                next_sibling = next_sibling.find_next_sibling()

        article_data = {
            "title": title,
            "subtitle": subtitle,
            "description": str(soup),
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
