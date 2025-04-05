from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Connect to the existing Chrome session
options = Options()
options.debugger_address = "127.0.0.1:9222"  # Connect to the debugging port

# Use existing Chrome session instead of opening a new one
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

print("✅ Connected to existing Chrome session!")
driver.get("https://medium.com")  # Example: Open Medium
time.sleep(3)  # Wait for Medium to load

## 📝 **Step 1: Click "Write" Button**
try:
    write_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Write')]")
    write_button.click()
    print("✅ Clicked 'Write' button")
    time.sleep(3)  # Wait for editor to load
except Exception as e:
    print(f"❌ Error clicking 'Write' button: {e}")
    driver.quit()
    exit()

# 🔹 **Article Data**
article_data = {
    "title": "At Ridhaav Hair Studio, Use Hair Extensions to Transform Your Look",
    "mainDescription": "Do you have dreams of adding volume to your hair or having long, beautiful locks? The easiest way to effortlessly get your preferred hairdo is using hair extensions. At Ridhaav Hair Studio, we're experts at creating beautiful hair extensions that go well with your natural hair to give you the self-assurance and look you deserve.",
}

# 📝 **Step 2: Enter Title**
try:
    wait = WebDriverWait(driver, 10)  # Wait for the title field to be available
    title_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[@data-testid='editorTitleParagraph']")
        )
    )

    title_input.click()  # Click to focus
    title_input.clear()  # Clear existing text
    title_input.send_keys(article_data["title"])  # Enter title
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    print("✅ Entered title and moved to content")
    time.sleep(2)

    # 🛠 **Fix Stale Element Issue: Re-locate <p> tag after pressing Enter**
    content_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@data-testid='editorParagraphText']")
        )
    )
    print("✅ Located content input")

except Exception as e:
    print(f"❌ Error entering title: {e}")
    driver.quit()
    exit()

# 📝 **Step 3: Enter Content**
try:
    content_input.click()  # Click to focus
    content_input.clear()  # Clear existing text
    content_input.send_keys(Keys.ENTER)
    time.sleep(1)
    editor = driver.find_element(
        By.XPATH, "(//p[@data-testid='editorParagraphText'])[2]"
    )

    # Inject HTML code
    html_content = """
    <p><strong>Types of Wigs:</strong></p>
    <ul>
        <li>Full Lace Wigs</li>
        <li>Front Lace Wigs</li>
        <li>U-Part Wigs</li>
    </ul>
    """
    driver.execute_script("arguments[0].innerHTML = arguments[1]", editor, html_content)
    time.sleep(1)
    editor.send_keys(Keys.ENTER)
    # content_input_02.send_keys(article_data["mainDescription"])
    print("✅ Entered content")
    time.sleep(2)

except Exception as e:
    print(f"❌ Error entering content: {e}")
    driver.quit()
    exit()

print("✅ Article drafted successfully!")
