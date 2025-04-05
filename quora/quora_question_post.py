from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# Set up Chrome to use an existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)  # Attach to existing browser
wait = WebDriverWait(driver, 15)

questions = [
    "What’s the difference between machine wefts and hand-tied wefts",
    "Are weft extensions suitable for thin or fine hair",
    "How often should I wash my weft hair extensions",
    "Do hair wefts cause scalp irritation",
    "Can I sleep with weft hair extensions in",
    "What's the best shampoo and conditioner for hair wefts",
    "How do I prevent my hair wefts from tangling",
    "Are there vegan or cruelty-free hair weft options",
    "How do I choose the right length for hair wefts",
    "What should I know before getting weft extensions for the first time",
    "Are invisible wefts better than traditional wefts",
    "Can I curl or straighten weft extensions like normal hair",
    "How much do salon-quality weft extensions cost",
    "What’s the difference between sew-in and glued-in wefts",
    "Will hair wefts blend with balayage or ombré styles",
]

SKIP_COUNT = int(input("Enter number of questions to skip: "))
questions = questions[SKIP_COUNT:]


def post_question_flow(selected_question):
    try:
        add_question_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[.//div[text()='Add question']])[1]")
            )
        )
        add_question_btn.click()
        print("Clicked 'Add Question'")
        time.sleep(3)

        # Check if "Edit Question" is visible first
        try:
            edit_question = driver.find_element(
                By.XPATH, "(//button[.//div[text()='Edit Question']])[1]"
            )
            print("❌ 'Edit Question' found – skipping this question.")
            return  # Skip to the next question

        except:
            pass

        # Check if "Use suggestion" is visible
        try:
            use_suggestion = driver.find_element(
                By.XPATH, "(//button[.//div[text()='Use suggestion']])[1]"
            )
            use_suggestion.click()
            print("✅ Clicked 'Use Suggestion'")
            time.sleep(9)

            # After using suggestion, click share icon 20 times
            for i in range(20):
                try:
                    share_icon = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "(//div[@class='q-relative puppeteer_popper_reference']//div[contains(@class, 'q-click-wrapper') and @tabindex='0'])[1]",
                            )
                        )
                    )
                    share_icon.click()
                    print(f"🔁 Clicked share icon {i + 1}/20")
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Error clicking share icon on try {i + 1}: {e}")
                    break

            try:
                done_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "(//button[.//div[text()='Done']])[1]")
                    )
                )
                done_button.click()
                print("✅ 'Done' button clicked after suggestion.")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Error clicking 'Done': {e}")
            return

        except:
            pass

        # If only share icon is visible
        time.sleep(8)
        try:
            for i in range(20):
                try:
                    share_icon = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "(//div[@class='q-relative puppeteer_popper_reference']//div[contains(@class, 'q-click-wrapper') and @tabindex='0'])[1]",
                            )
                        )
                    )
                    share_icon.click()
                    print(f"🔁 Clicked share icon directly {i + 1}/20")
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Error clicking share icon on try {i + 1}: {e}")
                    break

            try:
                done_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "(//button[.//div[text()='Done']])[1]")
                    )
                )
                done_button.click()
                print("✅ 'Done' button clicked directly after share.")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Error clicking 'Done': {e}")
        except Exception as e:
            print(f"⚠️ No valid path found after 'Add Question': {e}")

    except Exception as e:
        print(f"❌ Error posting question: {e}")


# Loop through each question
for selected_question in questions:
    print(f"\n➡️ Posting question: {selected_question}")
    driver.get("https://www.quora.com/")
    time.sleep(6)  # Wait for Quora homepage

    try:
        # Click "Add question"
        click_add = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@aria-label='Add question' and @aria-haspopup='dialog']",
                )
            )
        )
        click_add.click()
        print("Clicked 'Add question' button")
        time.sleep(3)

        # Type question
        ques_div = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@aria-expanded='true']")
            )
        )
        ques_div.click()
        time.sleep(2)
        ques_div.send_keys(selected_question)
        print(f"Entered question: {selected_question}")
        time.sleep(2)

        # Call the main question handling logic
        post_question_flow(selected_question)

    except Exception as e:
        print(f"❌ General error for question '{selected_question}': {e}")

    time.sleep(8)  # Delay before next question

print("\n✅ All questions processed.")
