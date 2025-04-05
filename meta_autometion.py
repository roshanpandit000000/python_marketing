import tkinter as tk
from tkinter import messagebox
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Facebook credentials
USERNAME = "ridhaavhair@gmail.com"
PASSWORD = "Google@ccount@123!@#"


def log_error(error_message):
    """Logs error messages to a file."""
    with open("error_log.txt", "a") as file:
        file.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")


def automate_meta_post():
    label_status.config(text="Opening Facebook...")
    root.update()

    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.facebook.com/")
        wait = WebDriverWait(driver, 20)

        label_status.config(text="Logging in...")
        root.update()

        # Wait for the username and password fields to be visible
        username_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        password_input = wait.until(EC.visibility_of_element_located((By.ID, "pass")))

        # Enter login credentials
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)

        # Wait for the Facebook homepage to load
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Facebook']"))
        )

        label_status.config(text="Login Successful!")
        root.update()

        click_post = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@role='button']//span[text()='Photo/video']']")
            )
        )
        click_post.click()

        messagebox.showinfo("Success", "Login successfully!")
    except Exception as e:
        error_message = traceback.format_exc()  # Capture full error details
        log_error(error_message)  # Log the error
        label_status.config(text="Error occurred!")
        messagebox.showerror("Error", error_message)  # Show error message in a popup

    finally:
        driver.quit()


# Create GUI
root = tk.Tk()
root.title("Meta Business Suite Auto Login")
root.geometry("400x250")

label_status = tk.Label(root, text="Status: Waiting", font=("Arial", 12))
label_status.pack(pady=20)

btn_login = tk.Button(root, text="Login to Meta", command=automate_meta_post)
btn_login.pack(pady=10)

root.mainloop()
