import time
import os
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Config
QUERY = "podcast"
JSON_FILE_PATH = (
    r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\youtube_channels.json"
)
SCROLL_TIMES = 100
WAIT_BETWEEN_SCROLLS = 2  # wait a bit more to ensure data loads

# Setup WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)


def load_existing_urls(filepath):
    """Load existing channel URLs from JSON file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return set(json.load(f))
    return set()


def save_urls_to_json(urls, filepath):
    """Save new unique URLs to the JSON file."""
    existing_urls = load_existing_urls(filepath)
    new_urls = [url for url in urls if url not in existing_urls]
    if new_urls:
        updated_urls = list(existing_urls.union(new_urls))
        with open(filepath, "w") as f:
            json.dump(updated_urls, f, indent=2)
        print(f"Saved {len(new_urls)} new channel(s).")
    else:
        print("No new channels to save.")


def scrape_channel_links():
    """Scrape unique YouTube channel links from current page."""
    xpath = "//a[@class='yt-simple-endpoint style-scope yt-formatted-string']"
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    print("List items loaded successfully.")
    elements = driver.find_elements(By.XPATH, xpath)
    links = set()
    for item in elements:
        href = item.get_attribute("href")
        if href and ("/channel/" in href or "@" in href):
            links.add(href.split("?")[0])  # remove query params
    return links


def scroll_and_scrape(times, wait):
    """Scroll, wait, scrape, check duplicates, save repeatedly."""
    for i in range(times):
        print(f"\nScroll iteration: {i + 1}")
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(wait)  # wait for new data to load

        new_links = scrape_channel_links()
        print(f"Scraped {len(new_links)} links so far.")

        save_urls_to_json(new_links, JSON_FILE_PATH)


def main():
    try:
        url = f"https://www.youtube.com/results?search_query={QUERY}"
        driver.get(url)
        time.sleep(3)  # wait for initial load

        # Start scrolling and scraping
        scroll_and_scrape(times=SCROLL_TIMES, wait=WAIT_BETWEEN_SCROLLS)

        print("Done!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
