from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Load the HTML content
with open("scraped_article.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# Find only h1 tag text
title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
time.sleep(2)
print("title filterd Successfull")

# Set up Chrome to use an existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=chrome_options)  # Attach to existing browser
driver.get("https://chat.openai.com/")  # Open ChatGPT in the same session
print("open chat successfull")
time.sleep(3)  # Wait for page to load

try:
    # Input the extracted title to ChatGPT
    input_box = driver.find_element(By.XPATH, "//div[@id='prompt-textarea']")
    input_box.click()
    time.sleep(4)
    print("Input Click Successfull")
    input_box.send_keys(f"Write an article about: {title} in sandbox")
    time.sleep(3)
    input_box.send_keys(Keys.RETURN)
    print("✅ Title extracted and sent to ChatGPT! Browser remains open.")
    # Wait for response to generate
    time.sleep(5)
    while True:
        try:
            completion_element = driver.find_element(
                By.XPATH,
                "//button[@data-testid='composer-speech-button']",
            )
            time.sleep(5)
            break  # Exit loop when found
        except:
            time.sleep(7)  # Keep checking until found

    print("article write successfull")

    # Scrap HTML from prosemirror editor container
    response_box = driver.find_element(
        By.XPATH,
        "//div[contains(@class, '_main_5jn6z_1') and contains(@class, 'markdown') and contains(@class, 'ProseMirror')]",
    )
    response_html = response_box.get_attribute("outerHTML")
    print("📝 ChatGPT Response HTML:")
    print("scrap chatgpt data")

    # Save HTML response to a file
    with open("chatgpt_response.html", "w", encoding="utf-8") as file:
        file.write(response_html)
    print("✅ HTML Response saved successfully!")
except Exception as e:
    print(f"⚠️ An error occurred: {e}")

# Keep the browser open
input("Press Enter to close the browser manually...")
