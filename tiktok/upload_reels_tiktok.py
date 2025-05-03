from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import json
import pyautogui
import re


# ====== USER INPUT ======
try:
    skip_count = int(input("Enter number of reels to skip: "))
    max_downloads = int(input("Enter max number of reels to download: "))
except ValueError:
    print("Invalid input. Please enter integers only.")
    exit()
# ========================

# Load existing data from reels_data.json
json_path = os.path.join(os.path.dirname(__file__), "reels_data.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        reels_data = json.load(f)
else:
    reels_data = []


# Set up Chrome options
options = Options()

# Point to your user data directory
options.add_argument(
    r"--user-data-dir=C:\Users\PcHelps\AppData\Local\Google\Chrome\User Data"
)
options.add_argument(
    "--profile-directory=Profile 7"
)  # Or 'Profile 1', 'Profile 2', etc.

# Optional: Keep browser open after script
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 15)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.debugger_address = "127.0.0.1:9222"
# driver = webdriver.Chrome(options=chrome_options)
# wait = WebDriverWait(driver, 15)


def keep_bmp_emojis(text):
    return "".join(c for c in text if ord(c) <= 0xFFFF)


def extract_caption_and_hashtags(text):
    hashtags = re.findall(r"#\w+", text)
    text_without_tags = re.sub(r"#\w+", "", text)
    return keep_bmp_emojis(text_without_tags.strip()), hashtags


try:
    driver.get("https://www.tiktok.com/tiktokstudio/upload")
    time.sleep(2)

    download_count = 0
    # Loop through each reel link
    for i, reel in enumerate(reels_data):
        if i < skip_count:
            print(f"⏭️ Skipping reel {i+1}: {reel['url']}")
            continue
        if download_count >= max_downloads:
            print("✅ Reached max download limit.")
            break

        try:
            filepath = reel["filepath"]
            caption = reel["caption"]

            upload_button = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[@aria-label='Select video']",
                    )
                )
            )
            upload_button.click()
            print("Clicking upload button...")
            time.sleep(2)
            print(f"Typing file path: {filepath}")
            pyautogui.write(filepath)
            time.sleep(2)
            pyautogui.press("enter")
            print("Pressing enter to upload")
            time.sleep(1)
            print("Waiting for caption field...")
            upload_caption = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@contenteditable='true']",
                    )
                )
            )
            upload_caption.click()
            print("caption input click")
            upload_caption.clear()
            print("Clear caption feild")
            time.sleep(1)
            main_caption, hashtags = extract_caption_and_hashtags(caption)
            print("Typing caption without hashtags...")
            time.sleep(1)
            upload_caption.send_keys(main_caption)
            print("Send input caption")
            time.sleep(2)
            # Send each hashtag one by one with dropdown selection
            for tag in hashtags:
                print(f"Typing hashtag: {tag}")
                upload_caption.send_keys(" " + tag)
                # time.sleep(1.5)  # wait for dropdown to show up
                try:
                    xpath_status = "(//div[@role='option'])[1]"
                    tiktok_tag = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_status))
                    )
                    tiktok_tag.click()
                    print(f"✅ Selected dropdown for: {tag}")
                except Exception as e:
                    print(f"⚠️ Could not select dropdown for {tag}: {e}")

            try:
                xpath_status = "//span[@data-testid='CheckCircleFill']"
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath_status))
                )
                print("Video... Uploded")
                print("Submit Video Successful, proceeding...")

                # Only wait for URL if "Submitting..." message is seen
                post = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@data-e2e='post_video_button']",
                        )
                    )
                )
                post.click()
                print("post button click")
                time.sleep(1)
                WebDriverWait(driver, 20).until(EC.url_contains("tiktokstudio/content"))
                download_count += 1
                time.sleep(1)

                plus_button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "(//button[@type='button' and @data-tt='Sidebar_Sidebar_Button'])[2]",
                        )
                    )
                )
                plus_button.click()
                time.sleep(1)

                WebDriverWait(driver, 20).until(EC.url_contains("tiktokstudio/upload"))

            except Exception as e:
                print(
                    "No 'Submitting...' message or URL didn't change — skipping wait."
                )

            print(f"⬇️ Uploading reel {i+1}: {reel['url']}")

        except Exception as inner_e:
            print(f"Error uploading reel {reel['url']}: {inner_e}")

except Exception as e:
    print(f"General error: {e}")
