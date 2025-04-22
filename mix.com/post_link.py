import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# API Endpoint for Articles
API_URL = "https://bellahararo.com/api/products"
response = requests.get(API_URL)
data = response.json()
products = data.get("allproducts", [])

# Exit if no articles
if not products:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()

SKIP_COUNT = int(input("Enter number of posts to skip: "))
products = products[SKIP_COUNT:]


for index, selected_products in enumerate(products, start=1):
    total = len(products)
    print(
        f"\n=== Submitting post {index} of {total}: {selected_products.get('slug', 'Untitled')} ==="
    )

    try:
        url = (
            "https://mix.com/add?url=https://bellahararo.com/shop/"
            + selected_products.get("slug", "")
        )

        driver.get(url)
        time.sleep(3)  # Wait for initial content to load
        xpath = '//input[@type="submit" and not(@disabled)]'
        submit_button = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, xpath)
        )
        submit_button.click()
        time.sleep(1)
        print("click Submit Button")

        try:
            xpath_status = '//div[@role="status" and @aria-live="polite" and contains(text(), "Submitting")]'
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, xpath_status))
            )
            print("Submitting... message appeared")

            # Only wait for URL if "Submitting..." message is seen
            WebDriverWait(driver, 25).until(EC.url_contains("liked_by=bellahararo"))
            print("Submit Article Successful, proceeding...")
            time.sleep(2)

        except Exception as e:
            print("No 'Submitting...' message or URL didn't change — skipping wait.")

    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_products.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
