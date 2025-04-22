import instaloader
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import json
import glob

# # Set up Chrome options
# options = Options()

# # Point to your user data directory
# options.add_argument(
#     r"--user-data-dir=C:\Users\PcHelps\AppData\Local\Google\Chrome\User Data"
# )
# options.add_argument(
#     "--profile-directory=Profile 7"
# )  # Or 'Profile 1', 'Profile 2', etc.

# # Optional: Keep browser open after script
# options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(service=Service(), options=options)


# ====== USER INPUT ======
try:
    skip_count = int(input("Enter number of reels to skip: "))
    max_downloads = int(input("Enter max number of reels to download: "))
except ValueError:
    print("Invalid input. Please enter integers only.")
    exit()
# ========================


chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)


# Scroll to load more reels
def scroll_until_enough_reels(driver, desired_count=10, delay=2, max_scrolls=50):
    collected = set()
    scrolls = 0
    while len(collected) < desired_count and scrolls < max_scrolls:
        reel_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/reel/')]")
        for elem in reel_elements:
            href = elem.get_attribute("href")
            if href and "/reel/" in href:
                collected.add(href)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        scrolls += 1
        print(f"📜 Scrolled {scrolls} times. Reels found: {len(collected)}")

    return list(collected)


save_dir = r"C:\Users\PcHelps\Documents\insta_reels"
os.makedirs(save_dir, exist_ok=True)

json_path = os.path.join(os.path.dirname(__file__), "reels_data.json")
# Initialize Instaloader
L = instaloader.Instaloader()

# Load existing data if any
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        reels_data = json.load(f)
else:
    reels_data = []


try:
    driver.get("https://www.instagram.com/bellahararo/reels/")
    time.sleep(2)

    reel_links = scroll_until_enough_reels(
        driver, desired_count=skip_count + max_downloads
    )
    print(f"Found {len(reel_links)} reels.")

    download_count = 0

    # Loop through each reel link
    for i, reel_url in enumerate(reel_links):
        if i < skip_count:
            print(f"⏭️ Skipping reel {i+1}: {reel_url}")
            continue
        if download_count >= max_downloads:
            print("✅ Reached max download limit.")
            break

        try:
            os.chdir(save_dir)  # Set working directory to insta_reels
            print(f"⬇️ Downloading reel {i+1}: {reel_url}")

            shortcode = reel_url.strip("/").split("/")[-1]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=f"{shortcode}_reel")

            # Look for actual .mp4 file inside the downloaded folder
            download_folder = os.path.join(save_dir, f"{shortcode}_reel")
            mp4_files = glob.glob(os.path.join(download_folder, "*.mp4"))

            if mp4_files:
                original_path = mp4_files[0]
                new_path = os.path.join(download_folder, f"{shortcode}.mp4")

                # Rename to shortcode.mp4 if needed
                if original_path != new_path:
                    os.rename(original_path, new_path)

                filepath = os.path.abspath(new_path).replace("\\\\", "\\")
            else:
                filepath = "N/A"

            reels_data.append(
                {"url": reel_url, "caption": post.caption, "filepath": filepath}
            )

            download_count += 1

        except Exception as inner_e:
            print(f"Error downloading reel {reel_url}: {inner_e}")

    # Save all data to JSON in the tiktok folder
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reels_data, f, indent=4, ensure_ascii=False)

    print("✅ All reel data saved to reels_data.json")

except Exception as e:
    print(f"General error: {e}")
