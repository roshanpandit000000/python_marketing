from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

# Initialize the WebDriver (ensure chromedriver is in your PATH)
# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)


try:
    # Navigate to Google
    driver.get("https://www.google.com")
    time.sleep(2)  # Wait for the page to load

    # Accept cookies if prompted (optional, depending on your location)
    try:
        accept_button = driver.find_element(By.XPATH, "//button[text()='I agree']")
        accept_button.click()
        time.sleep(2)
    except:
        pass  # If the accept button is not found, continue

    # Find the search box and enter the query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("site:bellahararo.com")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for results to load

    # Initialize a set to store unique URLs
    urls = set()

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
        )
        print("List items loaded successfully.")
    except:
        print("Timed out waiting for list items to load.")
        driver.quit()
        exit()

    # Loop through pages
    while True:
        time.sleep(1)
        # Find all search result elements
        search_results = driver.find_elements(By.CLASS_NAME, "MjjYud")
        # print("search:", search_results)

        # Extract href attributes and add to the set
        for result in search_results:
            try:
                a_tag = result.find_element(By.TAG_NAME, "a")
                url = a_tag.get_attribute("href")
                if url:
                    # print("url:", url)
                    urls.add(url)
            except:
                # Skip if <a> tag is not found in this block
                continue
        # Try to find the 'Next' button to go to the next page
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "pnnext"))
            )

            # Scroll into view
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                next_button,
            )
            time.sleep(0.5)  # Allow scroll animation

            driver.execute_script("arguments[0].click();", next_button)

            time.sleep(2)  # Wait for new results to load
        except Exception as e:
            # print(f"Could not click 'Next' button: {e}")
            print("✅ All Url Scrap Done")
            break  # No more pages

    # Convert the set to a list
    url_list = list(urls)

    import json
    import os

    # Define file path
    output_path = (
        r"C:\Users\PcHelps\Documents\Python\old_dead_index_link\dead_links.json"
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(url_list, f, indent=4)

    print(f"Saved {len(url_list)} URLs to {output_path}")

finally:
    # Close the browser
    driver.quit()
