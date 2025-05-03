import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile
from urllib.parse import urlparse
import mimetypes
from PIL import Image
import re
import requests
import os
import pyautogui


# API Endpoint for Articles
API_URL = "https://bellahararo.com/api/products"
response = requests.get(API_URL)
data = response.json()
products = data.get("allproducts", [])


SKIP_COUNT = int(input("Enter number of posts to skip: "))
MAX_POSTS = int(input("Enter the number of posts to submit: "))
products = products[SKIP_COUNT : SKIP_COUNT + MAX_POSTS]


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

# Exit if no articles
if not products:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()


try:
    driver.get("https://mastodon.social/publish")
    time.sleep(2)

    for index, selected_products in enumerate(products, start=1):

        total = len(products)
        print(
            f"\n=== Submitting post {index} of {total}: {selected_products.get('slug', 'Untitled')} ==="
        )

        try:

            slug = "https://bellahararo.com/shop/" + selected_products.get("slug", "")
            title = selected_products.get("name", "")
            image_urls = selected_products.get("images", [])
            temp_image_paths = []  # To store all temp image file paths
            for image_url in image_urls:
                print(f"Downloading Image: {image_url}")
                parsed_url = urlparse(image_url)
                ext = os.path.splitext(parsed_url.path)[-1].lower()

                if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
                    ext = ".jpg"

                response = requests.get(image_url)
                image_data = response.content

                if ext == ".webp":
                    with tempfile.NamedTemporaryFile(
                        suffix=".webp", delete=False
                    ) as temp_webp:
                        temp_webp.write(image_data)
                        temp_webp_path = temp_webp.name

                    with Image.open(temp_webp_path) as im:
                        rgb_im = im.convert("RGB")
                        fd, temp_image_path = tempfile.mkstemp(suffix=".jpg")
                        os.close(fd)
                        rgb_im.save(temp_image_path, "JPEG")
                    os.remove(temp_webp_path)
                else:
                    fd, temp_image_path = tempfile.mkstemp(suffix=ext)
                    os.close(fd)
                    with open(temp_image_path, "wb") as f:
                        f.write(image_data)

                temp_image_paths.append(temp_image_path)

            time.sleep(3)  # Wait for initial content to load

            try:
                # Type each image path and press 'enter'
                image_upload = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@aria-label='Add images, a video or an audio file']",
                        )
                    )
                )
                image_upload.click()
                time.sleep(2)
                pyautogui.write(os.path.dirname(temp_image_paths[0]))
                time.sleep(1)
                pyautogui.press("enter")
                time.sleep(1)
                file_names = [
                    f'"{os.path.splitext(os.path.basename(path))[0]}"'
                    for path in temp_image_paths
                ]
                pyautogui.write(" ".join(file_names))
                time.sleep(1)
                pyautogui.press("enter")

                print("✅ Image upload successful")

                main_text = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "(//textarea[@dir='auto'])[2]",
                        )
                    )
                )
                main_text.click()
                print("✅ Main text input clicked")
                main_text.clear()
                print("✅ Main text input cleared")
                main_text_input = (
                    title
                    + "\n"
                    + "#hair #hairextension #weft #hairstyle #style #women #men #fashion #beauty #haircare #hairproducts #haircolor #haircut #hairtransformation #hairinspo #hairtrends #hairlove #hairgoals #hairfashion #hairstylist #hairstyling #hairstyles"
                    + "\n"
                    + slug
                )
                main_text.send_keys(main_text_input)
                print("✅ Main text input filled")
                time.sleep(4)

                post_button = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "(//button[text()='Post'])[2]",
                        )
                    )
                )
                post_button.click()

                try:
                    while True:
                        # First check if post is already published
                        if driver.find_elements(
                            By.XPATH, "//span[text()='Post published.']"
                        ):
                            print("✅ Post published — moving to next post")
                            break

                        # Find all 'Add alt text' buttons
                        alt_buttons = driver.find_elements(
                            By.XPATH, "//button[text()='Add alt text']"
                        )

                        if not alt_buttons:
                            print(
                                "❌ No 'Add alt text' buttons left and post not published."
                            )
                            break

                        print(f"📝 Found {len(alt_buttons)} 'Add alt text' buttons")

                        # Click each 'Add alt text' button and fill the title
                        for i, alt_button in enumerate(alt_buttons):
                            try:
                                alt_button.click()
                                print(f"📝 ALT button clicked for image {i+1}")

                                image_alt_input = wait.until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//textarea[@id='description']")
                                    )
                                )
                                image_alt_input.click()
                                image_alt_input.send_keys(title)
                                print("✅ ALT input filled")

                                time.sleep(0.5)

                                image_alt_input_done = wait.until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//button//span[text()='Done']")
                                    )
                                )
                                image_alt_input_done.click()
                                print("✅ ALT input submitted")

                                time.sleep(1)

                                # Click Post button if available
                                post_buttons = driver.find_elements(
                                    By.XPATH, "(//button[text()='Post'])"
                                )
                                if len(post_buttons) > 1:
                                    post_buttons[1].click()
                                    print("✅ Post button clicked")

                            except Exception as e:
                                print(f"⚠️ Failed to process one ALT: {e}")
                                continue

                        # Short pause before re-checking for alt buttons or post status
                        time.sleep(2)

                except Exception as e:
                    print(f"⚠️ ALT/post publishing loop failed: {e}")
                    continue

                print("✅ Submit Article Successful, proceeding...")
                time.sleep(2)

            except Exception as e:
                print(
                    "No 'Submitting...' message or URL didn't change — skipping wait."
                )

        except Exception as e:
            print(
                f"Error submitting article {index} ({selected_products.get('title')}): {e}\n"
            )

except Exception as e:
    print(f"General error: {e}")

time.sleep(5)  # Wait for the page to load before closing the driver
