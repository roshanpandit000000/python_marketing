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


driver.get("https://hubpages.com/hubtool/edit/6553329")
time.sleep(5)  # Wait for initial content to loa


summary = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[@title='Click to edit summary']"))
)
summary.click()
print(f"Click 'Summary' Input")
time.sleep(1)
textarea = wait.until(
    EC.presence_of_element_located((By.XPATH, "//textarea[@maxlength='300']"))
)
textarea.send_keys(
    "Discover why weft hair extensions are a must-have beauty secret for supermodels like Adriana Lima. From adding instant volume and length to achieving flawless, runway-ready hair, this guide reveals how weft extensions help create her signature glamorous look."
)
print(f"Send 'textarea' Input")
time.sleep(1)

bio = wait.until(EC.presence_of_element_located((By.ID, "hubBioId")))
select_option = Select(bio)
select_option.select_by_value("381212")
print(f"Select 'Option' Input")
time.sleep(1)

edite_photo = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/div[2]/div[2]/div[3]/div[7]/div/div[2]/div[2]/div[2]",
        )
    )
)
print("Edit photo found")
print("Displayed:", edite_photo.is_displayed(), " | Enabled:", edite_photo.is_enabled())
time.sleep(1)
edite_photo.click()
print("Edit photo clicked")
time.sleep(1)

inser_photo = wait.until(EC.presence_of_element_located((By.ID, "photo_insert_import")))
inser_photo.click()
time.sleep(1)

inser_photo_input = wait.until(EC.presence_of_element_located((By.ID, "url_0")))
inser_photo_input.click()
time.sleep(1)
inser_photo_input.send_keys(
    "https://res.cloudinary.com/dx0rnjybh/image/upload/v1743764916/574ff1c7a337a72b8288bb468dcc1619_pxyjvz.jpg"
)
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
        EC.presence_of_element_located((By.XPATH, "//a[@title='Save this Capsule']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_image)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", save_image)
    time.sleep(4)

edite_text = wait.until(EC.presence_of_element_located((By.ID, "modempty_57077247")))
time.sleep(1)
print("Edit text found")
edite_text.click()
time.sleep(1)

html_code = "<p>Weft hair extensions are a game-changer for supermodels like Adriana Lima. They add instant volume and length, allowing for stunning hairstyles that turn heads on the runway. This guide reveals how weft extensions help create her signature glamorous look.</p>"

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
time.sleep(1)
html_input.send_keys(html_code)
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
    EC.presence_of_element_located((By.XPATH, "//a[@title='Save this Capsule']"))
)
save_html.click()
print("Save HTML clicked in main page")
time.sleep(4)

disclamer = wait.until(EC.presence_of_element_located((By.ID, "disclaimer_control")))
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
publish.click()
print("Publish clicked")
time.sleep(5)


# Switch back to the default content
print("All inputs filled successfully!")


time.sleep(5)  # Wait for the page to load before closing the driver
