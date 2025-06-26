import time
import json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

JSON_FILE_PATH = (
    r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\youtube_channels.json"
)
SOCIAL_LINKS_JSON_PATH = (
    r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\social_links.json"
)

# Setup WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)


def load_urls(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def extract_social_links(channel_url):
    """Extract social media links from the About section of a YouTube channel."""
    links_data = []
    try:
        last_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )
        for _ in range(3):  # Adjust scroll attempts as needed
            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
            )
            time.sleep(1)  # Give time to load
            new_height = driver.execute_script(
                "return document.documentElement.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
            
        external_links = driver.find_elements(
            By.XPATH, "//yt-channel-external-link-view-model"
        )
        for el in external_links:
            platform = el.find_element(
                By.CLASS_NAME, "yt-channel-external-link-view-model-wiz__title"
            ).text
            url_el = el.find_element(
                By.XPATH, ".//a[contains(@class, 'yt-core-attributed-string__link')]"
            )
            url = url_el.get_attribute("href")
            links_data.append({"platform": platform, "url": url})
    except Exception as e:
        print(f"Failed to extract social links: {e}")
    # ✅ Return with channel URL
    return channel_url, links_data


def save_to_json(channel_url, links, file_path):
    """Save the extracted data to a JSON file grouped by channel URL."""
    existing = {}

    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                if content:
                    existing = json.loads(content)
        except json.JSONDecodeError:
            print(f"Warning: {file_path} is not valid JSON. Starting fresh.")

    # Add or update links for the current channel
    if channel_url not in existing:
        existing[channel_url] = []

    existing_links = {entry["url"]: entry for entry in existing[channel_url]}
    for entry in links:
        existing_links[entry["url"]] = entry

    existing[channel_url] = list(existing_links.values())

    with open(file_path, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"Saved {len(links)} links for {channel_url}.")


def open_links_one_by_one(links, wait_time=5):
    for url in links:
        try:
            print(f"Opening: {url}")
            driver.get(f"{url}/about")
            time.sleep(2)

            try:
                more_button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[contains(@class, 'truncated-text-wiz__absolute-button') and .//span[text()='...more']]",
                        )
                    )
                )
                more_button.click()
            except:
                pass  # no "...more" button

            # ✅ Pass URL to extract
            channel_url, links_data = extract_social_links(url)
            # ✅ Pass channel_url to save function
            save_to_json(channel_url, links_data, SOCIAL_LINKS_JSON_PATH)
            time.sleep(wait_time)

        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue


def main():
    try:
        urls = load_urls(JSON_FILE_PATH)
        open_links_one_by_one(urls, wait_time=5)
        print("Finished extracting all social links.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
