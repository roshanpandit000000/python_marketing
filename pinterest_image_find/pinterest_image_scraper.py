from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from difflib import SequenceMatcher
from urllib.parse import quote_plus
import time
import json
import os


options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome()

title_text = "hot women"
encoded_query = quote_plus(title_text)
search_url = f"https://www.pinterest.com/search/pins/?q={encoded_query}"
driver.get(search_url)

assert "Pinterest" in driver.title

all_images = set()
image_data = []
scroll_attempts = 0
max_scrolls = 25
output_file = "pinterest_images.json"

if os.path.exists(output_file):
    with open(output_file, "r") as f:
        try:
            image_list = json.load(f)
            unique_images = set(image_list)
        except json.JSONDecodeError:
            image_list = []
            unique_images = set()

while scroll_attempts < max_scrolls:
    print(f"\nScroll attempt {scroll_attempts + 1}...")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='listitem']"))
        )
        print("List items loaded successfully.")
    except:
        print("Timed out waiting for list items to load.")
        driver.quit()
        exit()

    list_items = driver.find_elements(By.XPATH, "//div[@role='listitem']")
    print(f"Found {len(list_items)} list items.")
    new_urls_found = 0

    for item in list_items:
        try:
            img = item.find_element(By.TAG_NAME, "img")
            srcset = img.get_attribute("srcset")
            if srcset:
                srcset_urls = srcset.split(", ")
                for url in srcset_urls:
                    if "originals" in url:
                        original_url = url.split(" ")[0]
                        if original_url not in all_images:
                            unique_images.add(original_url)
                            image_list.append(original_url)
                            new_urls_found += 1
                            print(f"Found image: {original_url}")
        except:
            continue  # Skip any listitem that doesn't have an image
    # Save after each scroll
    with open(output_file, "w") as f:
        json.dump(image_list, f, indent=4)
    print(f"Saved {len(image_list)} total images (new this scroll: {new_urls_found})")

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    scroll_attempts += 1

print(f"\n✅ Completed. Total unique original image URLs saved: {len(image_list)}")

# assert "No results found." not in driver.page_source
input("Press Enter to close the driver...")
# driver.quit()
