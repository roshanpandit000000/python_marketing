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


def google_trends():
    countries = ["US", "IT", "BR"]

    print("Available countries:")
    for i, code in enumerate(countries):
        print(f"{i}: {code}")

    try:
        selection = int(
            input("Choose number of the country (0 for US, 1 for IT, 2 for BR): ")
        )
        if selection not in range(len(countries)):
            raise ValueError("Invalid selection.")
        country_input = countries[selection]
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        exit()

    try:
        url = f"https://trends.google.com/trending?geo={country_input}&hours=168&sort=search-volume&status=active"
        driver.get(url)
        time.sleep(random.uniform(2.5, 4.5))  # Wait for initial content to load
        print("open trends successfull")

        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[@jsaction]"))
        )

        scraped_data = []

        while True:
            rows = driver.find_elements(By.XPATH, "//tr[@jsaction]")
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) >= 5:
                    col_2 = tds[1].text.strip()
                    col_5_raw = tds[4].text.strip()

                    # Remove "+ xxx more" and split by newlines
                    col_5_lines = col_5_raw.split("\n")
                    col_5_cleaned = [
                        line.strip()
                        for line in col_5_lines
                        if not line.startswith("+") and line.strip()
                    ]

                    item = {"column_2": col_2, "column_5": col_5_cleaned}
                    scraped_data.append(item)

            # Try to click the "Next Page" button
            try:
                next_button = driver.find_element(
                    By.XPATH, "//button[@aria-label='Go to next page']"
                )
                if next_button.is_enabled():
                    driver.execute_script("arguments[0].click();", next_button)
                else:
                    print("Next button disabled. Ending pagination.")
                    break
            except Exception as e:
                print(f"No more pages or error clicking next: {e}")
                break

        with open(
            r"C:\Users\PcHelps\Documents\Python\Deepseek_article_scraper\google_trends.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(scraped_data, f, indent=4, ensure_ascii=False)

        print(f"Scraped and saved {len(scraped_data)} records to trends_data.json")

    except Exception as e:
        print(f"Error submitting article: {e}\n")


def deepseek():
    try:
        url = f"https://chat.deepseek.com/"
        driver.get(url)
        time.sleep(random.uniform(2.5, 4.5))  # Wait for initial content to load
        print("open trends successfull")

        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.ID, "chat-input"))
        )

        input_box = wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "chat-input",
                )
            )
        )
        input_box.click()
        time.sleep(random.uniform(1.5, 2.5))
        print("Input Click Successfull")

        input_box.send_keys(
            f"Write an professional article about: hair extesnion for backlinking purpose. "
            f"Make sure to include these links in the article: https://bellahararo.com."
        )
        time.sleep(random.uniform(1.5, 3.5))
        input_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(1.5, 3.5))

        xpath_status = "//div[@role='button' and @aria-disabled='true']"
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath_status))
        )
        print("✅ Submit Article Successful, proceeding...")

        response_box = None  # Initialize
        response_html = ""
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'ds-markdown')]",
                    )
                )
            )
            response_boxes = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'ds-markdown')]",
            )
            print("✅ ProseMirror response boxes found.")
        except TimeoutException:
            print("⚠️ ProseMirror not found in 2 seconds. Trying fallback selector...")

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

        article_data = {
            # "title": title,
            # "subtitle": subtitle,
            # "image": original_url,
            "description": response_html,
            # "slug": links[0] if links else "",
        }

        with open(
            r"C:\Users\PcHelps\Documents\Python\Deepseek_article_scraper\deepseek_article.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(article_data, f, indent=4, ensure_ascii=False)

        print(f"Scraped and saved records to trends_data.json")

    except Exception as e:
        print(f"Error submitting article: {e}\n")


deepseek()
