from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import time

# Set up Chrome to use an existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

driver.get("https://www.quora.com/search?q=hair%20extension&time=month&type=question")


# Function to scroll to bottom and wait for more content to load
def scroll_to_bottom(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

        # Wait for new page height after scroll
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # No more new content
        last_height = new_height


# Scroll through the page to load all results
print("Scrolling through the page to load all questions...")
scroll_to_bottom(driver)
print("Finished scrolling.")

# Wait for elements to load (final assurance)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "qu-userSelect--text")))

# Extract and de-duplicate text
text_elements = driver.find_elements(By.CLASS_NAME, "qu-userSelect--text")
seen = set()
questions = []

for idx, element in enumerate(text_elements, start=1):
    text = element.text.strip()
    if text and text not in seen:
        seen.add(text)
        questions.append({"question_number": len(questions) + 1, "question_text": text})

# Save to JSON
with open("scraped_questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

print(f"Scraping complete. Saved {len(questions)} questions to scraped_questions.json")
