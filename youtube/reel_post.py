import yt_dlp
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Set up Chrome options
options = Options()

# Point to your user data directory
options.add_argument(
    r"--user-data-dir=C:\Users\PcHelps\AppData\Local\Google\Chrome\User Data"
)
options.add_argument("--profile-directory=Default")  # Or 'Profile 1', 'Profile 2', etc.

# Optional: Keep browser open after script
options.add_experimental_option("detach", True)

# Launch Chrome
driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 15)
# Go to YouTube
driver.get("https://www.youtube.com")

try:
    short = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Shorts']"))
    )
    short.click()
    time.sleep(2)


except Exception as e:
    print(f"Error submitting article): {e}\n")
