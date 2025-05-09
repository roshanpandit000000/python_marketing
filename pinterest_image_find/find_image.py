from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from difflib import SequenceMatcher
from urllib.parse import quote_plus
import time


def is_similar(a, b, threshold=0.4):
    similarity = SequenceMatcher(None, a.lower(), b.lower()).ratio()
    # print(f"Similarity between:\n  A: '{a}'\n  B: '{b}'\n  ➤ Score: {similarity:.2f}")
    return similarity >= threshold


def word_overlap_ratio(a, b, threshold=0.5):
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    overlap = set_a & set_b
    ratio = len(overlap) / len(set_a) if set_a else 0
    # print(f"Word Overlap: {overlap} ➤ Ratio: {ratio:.2f}")
    return ratio >= threshold


options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome()

title_text = "This new IDE from Google is an absolute game changer"
encoded_query = quote_plus(title_text)
search_url = f"https://www.pinterest.com/search/pins/?q={encoded_query}"
driver.get(search_url)

assert "Pinterest" in driver.title

found_match = False
scroll_attempts = 0
max_scrolls = 10


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
    # print(f"Found {len(list_items)} list items.")

    for item in list_items:
        try:
            img = item.find_element(By.TAG_NAME, "img")
            alt_text = img.get_attribute("alt")

            if alt_text and (
                is_similar(title_text, alt_text)
                or word_overlap_ratio(title_text, alt_text)
            ):

                srcset = img.get_attribute("srcset")
                if srcset:
                    srcset_urls = srcset.split(", ")
                    original_url = None
                    for url in srcset_urls:
                        if "originals" in url:
                            original_url = url.split(" ")[0]
                            break
                print(f"Matched ALT: {alt_text}")
                print(f"Image SRC: {original_url}")
                found_match = True
                break  # Stop after first match
        except:
            continue  # Skip any listitem that doesn't have an image

    if not found_match:
        print("❌ No match found this round. Scrolling for more...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        scroll_attempts += 1
    else:
        print("✅ Match found. Stopping further search.")
        break

    # Scroll to load more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    scroll_attempts += 1

if not found_match:
    print("😢 No matching images found after scrolling.")
# assert "No results found." not in driver.page_source
input("Press Enter to close the driver...")
# driver.quit()
