import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import requests


# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# API Endpoint for Articles
API_URL = "https://bellahararo.com/api/article"
response = requests.get(API_URL)
data = response.json()
articles = data.get("articles", [])

# Exit if no articles
if not articles:
    print("No articles found from the API. Exiting.")
    driver.quit()
    exit()

SKIP_COUNT = int(input("Enter number of posts to skip: "))
articles = articles[SKIP_COUNT:]


def extract_clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove all <img>, <video>, <iframe>, <script>, and <style> tags
    for tag in soup(["img", "video", "iframe", "script"]):
        tag.decompose()

    # Remove elements that mention "video" in their text (e.g., "Watch this video")
    for tag in soup.find_all(string=lambda s: s and "video" in s.lower()):
        parent = tag.find_parent()
        if parent:
            parent.decompose()

    # Remove extra <br> tags (reduce multiple <br><br><br> to a single <br>)
    for parent in soup.find_all():
        brs = parent.find_all("br")
        if len(brs) > 1:
            previous = None
            for br in brs:
                if previous and previous.name == "br":
                    br.extract()  # remove the extra one
                else:
                    previous = br

        # Remove characters outside the Basic Multilingual Plane (U+0000 to U+FFFF)
    cleaned_html = "".join(c for c in str(soup) if ord(c) <= 0xFFFF)

    return cleaned_html


for index, selected_article in enumerate(articles, start=1):
    total = len(articles)
    print(
        f"\n=== Submitting Article {index} of {total}: {selected_article.get('title', 'Untitled')} ==="
    )

    article_data = {
        "title": selected_article.get("title", ""),
        "mainDescription": selected_article.get("mainDescription", ""),
        "image_url": selected_article.get("images", ""),
        "subtitle": selected_article.get("shortDescription", ""),
    }

    try:
        driver.get("https://hubpages.com/hubtool/create/name/")
        time.sleep(5)  # Wait for initial content to load

        title = wait.until(EC.presence_of_element_located((By.ID, "title")))
        title.click()
        time.sleep(1)
        title.send_keys(article_data["title"])
        print(f"Send 'Title' Input")
        time.sleep(1)

        browser = wait.until(
            EC.presence_of_element_located((By.ID, "tab_categoryTabs_0"))
        )
        browser.click()
        time.sleep(1)

        select_element = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "select"))
        )
        select_option = Select(select_element)
        select_option.select_by_value("1117")
        print(f"Select 'Option' Input")
        category_name = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "category_name"))
        )
        time.sleep(1)
        if category_name.is_displayed():
            print("Category name is displayed")
            time.sleep(3)

            # Re-fetch the <select> element after the DOM update
            select_element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "select"))
            )
            subcategory = Select(select_element)
            subcategory.select_by_value("1256")
            print(f"Select 'subcategory' Input")
            time.sleep(2)

            # Re-fetch again if needed before the next interaction
            select_element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "select"))
            )
            subcategory = Select(select_element)
            subcategory.select_by_value("1268")
        else:
            print("Category name is not displayed")
        print("Category selected")
        time.sleep(2)

        layout = wait.until(EC.presence_of_element_located((By.ID, "TIC")))
        print("Layout found")
        time.sleep(1)
        layout.click()
        time.sleep(1)
        print("Layout clicked")

        frames = driver.find_elements(By.TAG_NAME, "iframe")
        print("Frames found")
        time.sleep(1)
        # Switch to reCAPTCHA frame
        for frame in frames:
            if "reCAPTCHA" in frame.get_attribute("title"):
                driver.switch_to.frame(frame)
                break

        checkbox = wait.until(
            EC.presence_of_element_located((By.ID, "recaptcha-anchor"))
        )
        checkbox.click()
        print("Checkbox clicked")
        time.sleep(3)

        driver.switch_to.default_content()

        continu_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@class='button primary_action' and @type='button']")
            )
        )
        print("Continue button found and clickable")
        time.sleep(1)

        try:
            continu_button.click()
        except Exception as e:
            print("Standard click failed, using JS click instead")
            driver.execute_script("arguments[0].click();", continu_button)

        time.sleep(5)
        print("Continue button clicked, waiting for hubtool page to load...")

        WebDriverWait(driver, 30).until(EC.url_contains("hubtool"))
        print("Hubtool page loaded, continuing with next steps...")

        time.sleep(3)  # Wait for the page to load
        summary = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@title='Click to edit summary']")
            )
        )
        summary.click()
        print(f"Click 'Summary' Input")
        time.sleep(1)
        textarea = wait.until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@maxlength='300']"))
        )
        textarea.send_keys(article_data["subtitle"])
        print(f"Send 'textarea' Input")
        time.sleep(1)

        bio = wait.until(EC.presence_of_element_located((By.ID, "hubBioId")))
        select_option = Select(bio)
        select_option.select_by_value("381212")
        print(f"Select 'Option' Input")
        time.sleep(1)

        driver.switch_to.default_content()

        edite_photo = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[3]/div[7]/div/div[2]/div[2]/div[2]",
                )
            )
        )
        print("Edit photo found")
        print(
            "Displayed:",
            edite_photo.is_displayed(),
            " | Enabled:",
            edite_photo.is_enabled(),
        )
        time.sleep(1)
        edite_photo.click()
        print("Edit photo clicked")
        time.sleep(1)

        inser_photo = wait.until(
            EC.presence_of_element_located((By.ID, "photo_insert_import"))
        )
        inser_photo.click()
        time.sleep(1)

        inser_photo_input = wait.until(EC.presence_of_element_located((By.ID, "url_0")))
        inser_photo_input.click()
        time.sleep(1)
        inser_photo_input.send_keys(article_data["image_url"])
        print(f"Send 'Image' Input")
        time.sleep(1)

        import_photo = wait.until(
            EC.presence_of_element_located((By.ID, "photo_import_submit"))
        )
        import_photo.click()
        time.sleep(1)

        source_image = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[text()='Name of source (optional):']")
            )
        )

        if source_image.is_displayed():
            print("Image source is displayed")
            time.sleep(2)
            save_image = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[@title='Save this Capsule']")
                )
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", save_image
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", save_image)
            time.sleep(4)
        else:
            print("Image source not displayed, discarding changes...")
            discard_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//a[@title='Discard changes'])[1]")
                )
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", discard_button
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", discard_button)
            time.sleep(2)

        edite_text = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[3]/div[7]/div/div[3]/div[2]/div[2]",
                )
            )
        )
        time.sleep(1)
        print("Edit text found")
        edite_text.click()
        time.sleep(1)

        html_text = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@role='button' and @title='Edit HTML Source']")
            )
        )
        print("Edit HTML source found")
        html_text.click()
        time.sleep(1)

        # ✅ Switch to iframe where the HTML editor is loaded
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_1_ifr")))
        print("Switched to HTML editor iframe")

        html_input = wait.until(EC.presence_of_element_located((By.ID, "htmlSource")))
        time.sleep(1)
        print("HTML source found")
        html_input.click()
        print("HTML input clicked")
        time.sleep(1)
        html_input.clear()
        print("HTML input cleared")
        html_description = selected_article.get("mainDescription", "")
        plain_text_description = extract_clean_html(html_description)
        time.sleep(3)
        html_input.send_keys(plain_text_description)
        print(f"Send 'HTML' Input")
        time.sleep(1)
        save_html = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='button' and @value='save']")
            )
        )
        save_html.click()
        print("Save HTML clicked")
        time.sleep(2)

        # ✅ Back to the main page
        driver.switch_to.default_content()

        save_html = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@title='Save this Capsule']")
            )
        )
        save_html.click()
        print("Save HTML clicked in main page")
        time.sleep(4)

        disclamer = wait.until(
            EC.presence_of_element_located((By.ID, "disclaimer_control"))
        )
        select_option = Select(disclamer)
        select_option.select_by_value("3")
        print(f"Select 'disclamer' Option")
        time.sleep(1)

        copyright = wait.until(EC.presence_of_element_located((By.ID, "addCopyright")))
        select_option = Select(copyright)
        select_option.select_by_value("1")
        print(f"Select 'copyright' Option")
        time.sleep(2)

        publish = wait.until(EC.presence_of_element_located((By.ID, "Publish_btn")))
        print("Publish found")
        time.sleep(1)
        print(
            "Displayed:",
            publish.is_displayed(),
            " | Enabled:",
            publish.is_enabled(),
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", publish
        )
        time.sleep(1)
        driver.execute_script(
            "arguments[0].click();", publish
        )  # JS click bypasses overlays
        print("Publish clicked")
        time.sleep(5)

        print("Continue Published  button clicked, waiting for hubtool page to load...")

        WebDriverWait(driver, 30).until(EC.url_contains("style"))
        print("articel publish successfull, continuing to upload next article...")
        time.sleep(5)
    except Exception as e:
        print(
            f"Error submitting article {index} ({selected_article.get('title')}): {e}\n"
        )

time.sleep(5)  # Wait for the page to load before closing the driver
