import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load questions + answers from JSON
with open("scraped_questions.json", "r", encoding="utf-8") as f:
    saved_data = json.load(f)

# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# Go to Quora search page
driver.get("https://www.quora.com/search?q=hair%20extension&time=month&type=question")
time.sleep(5)  # Wait for initial content to load

# Get all visible question texts in order
question_elements = driver.find_elements(By.CLASS_NAME, "qu-userSelect--text")
page_questions = [el.text.strip() for el in question_elements if el.text.strip()]

# Loop through visible questions on the page
# Loop through visible questions on the page
for page_index, page_question in enumerate(page_questions, start=1):
    matched_q = next(
        (q for q in saved_data if q["question_text"].strip() == page_question), None
    )

    if matched_q:
        print(f"Match found for: '{matched_q['question_text']}' at index {page_index}")
        # print(f"Question Number: {matched_q['question_number']}")
        try:
            # Try clicking the corresponding Answer button
            answer_btn_xpath = f"(//button[.//div[text()='Answer']])[1]"
            try:
                answer_btn = wait.until(
                    EC.element_to_be_clickable((By.XPATH, answer_btn_xpath))
                )
                answer_btn.click()
                print(f"Clicked 'Answer' for: {matched_q['question_text']}")
                time.sleep(3)
            except Exception:
                print(f"Answer already submitted for Q{matched_q['question_number']}")
                continue  # Skip to next question

            # Find the input field and send the answer
            answer_input = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-kind='doc' and @contenteditable='true']")
                )
            )
            answer_input.click()
            time.sleep(1)
            answer_input.send_keys(matched_q["answer"])
            print(f"Typed answer: {matched_q['answer'][:60]}...")
            time.sleep(1)

            # Click the Post button
            post_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[.//div[text()='Post']])[1]")
                )
            )
            post_btn.click()
            print("Clicked 'Post'")
            time.sleep(3)

            # Click the Done button
            done_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[.//div[text()='Done']])[1]")
                )
            )
            done_btn.click()
            print("Clicked 'Done'")
            time.sleep(5)

            if (
                "https://www.quora.com/" in driver.current_url
                and "answer" in driver.current_url
            ):
                print("Redirected to post view, going back...")
                driver.back()
                time.sleep(5)

                # Re-fetch question list after returning to search page
                question_elements = driver.find_elements(
                    By.CLASS_NAME, "qu-userSelect--text"
                )
                page_questions = [
                    el.text.strip() for el in question_elements if el.text.strip()
                ]

        except Exception as e:
            print(f"Error while answering Q{matched_q['question_number']}: {e}")
    else:
        print(f"No match found for: '{page_question}'")
