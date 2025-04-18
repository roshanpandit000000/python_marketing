import pyautogui
import tkinter as tk
from tkinter import messagebox, filedialog
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Instagram credentials
USERNAME = "ridhaavhairstudio"
PASSWORD = "Aav@114"


def log_error(error_message):
    """Logs error messages to a file."""
    with open("error_log.txt", "a") as file:
        file.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")


def on_button_click():
    file_path = entry_file.get()
    caption = entry_caption.get()
    location = entry_location.get()
    alt_text = entry_alt.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return
    automate_instagram_post(file_path, caption, location, alt_text)


def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Media Files", "*.jpg;*.png;*.mp4")]
    )
    # if file_path:
    #     # Convert to forward slashes and add quotes
    #     formatted_path = f'"{file_path.replace("\\", "/")}"'

    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)


def automate_instagram_post(file_path, caption, location, alt_text):
    label_status.config(text="Opening Instagram...")
    root.update()

    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.instagram.com/accounts/login/")
        wait = WebDriverWait(driver, 15)

        label_status.config(text="Logging in...")
        root.update()

        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)

        label_status.config(text="Login Successful...")

        try:
            not_now_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(), 'Not now')]")
                )
            )
            not_now_button.click()
        except:
            pass  # Ignore if the button isn't found

        label_status.config(text="Navigating to Home Page...")
        root.update()

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Home')]")
            )
        )

        label_status.config(text="Uploading Post...")
        root.update()

        # Click the Create Post button
        create_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[7]/div/span/div/a/div/div[2]""",
                )
            )
        )
        create_button.click()

        time.sleep(3)

        post_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[7]/div/span/div/div/div/div[1]/a[1]""",
                )
            )
        )
        post_button.click()

        time.sleep(5)

        Select_from_computer = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[text()='Select from computer']",
                )
            )
        )
        Select_from_computer.click()

        time.sleep(5)

        formatted_path = f'"{file_path.replace("/", "\\")}"'
        # Use PyAutoGUI to type file path and press Enter
        pyautogui.write(formatted_path)  # Type the file path
        time.sleep(1)  # Small delay
        pyautogui.press("enter")  # Press Enter

        label_status.config(text="Uploading Image...")
        root.update()

        select_original_size = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[9]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button""",
                )
            )
        )
        select_original_size.click()

        time.sleep(2)

        original_size = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[9]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/div[1]""",
                )
            )
        )
        original_size.click()

        close_original_size = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[9]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button""",
                )
            )
        )
        close_original_size.click()

        click_next = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(text(), 'Next')]",
                )
            )
        )
        click_next.click()

        click_again_next = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(text(), 'Next')]",
                )
            )
        )
        click_again_next.click()

        caption_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    """//div[@aria-label='Write a caption...']""",
                )
            )
        )
        caption_input.click()

        actions = ActionChains(driver)
        actions.move_to_element(caption_input).click().send_keys(caption).perform()

        location_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    """//input[@type='text' and @placeholder='Add location']""",
                )
            )
        )
        location_input.send_keys(location)

        wait = WebDriverWait(driver, 10)
        Accessibility_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and contains(., 'Accessibility')]")
            )
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView();", Accessibility_button)

        # Click the element
        try:
            Accessibility_button.click()
        except:
            # If normal click fails, use JavaScript click
            driver.execute_script("arguments[0].click();", Accessibility_button)

        alt_text_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, """//input[@placeholder='Write alt text...']""")
            )
        )
        alt_text_input.send_keys(alt_text)

        # Wait until the accordion button is clickable
        wait = WebDriverWait(driver, 10)
        advance_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and contains(., 'Advanced settings')]")
            )
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView();", advance_option)

        # Click the element
        try:
            advance_option.click()
        except:
            # If normal click fails, use JavaScript click
            driver.execute_script("arguments[0].click();", advance_option)

        # Wait until the accordion button is clickable
        wait = WebDriverWait(driver, 10)
        checkbox_element = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(., 'Automatically share to Threads')]",
                )
            )
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView();", checkbox_element)

        try:
            checkbox_xpath = """//span[contains(text(), 'Automatically share to Threads')]/ancestor::div[2]//input[@role='switch']"""
            checkbox_element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
            )

            # Check if the checkbox is unchecked
            is_checked = checkbox_element.get_attribute("aria-checked") == "true"

            if not is_checked:
                driver.execute_script(
                    "arguments[0].click();", checkbox_element
                )  # Force click
                print("✅ Checkbox enabled.")
            else:
                print("⚡ Checkbox is already enabled.")

        except Exception as e:
            print(
                f"🚀 Checkbox not found or could not be clicked, skipping... Error: {e}"
            )

        share_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """//div[@role='button' and text()='Share']""",
                )
            )
        )
        share_button.click()

        # Wait until the success message appears (max 10 seconds)
        wait = WebDriverWait(driver, 10)
        success_message = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[text()='Your post has been shared.']")
            )
        )

        print("✅ Post shared successfully!")

        label_status.config(text="Login Successfully!")
        root.update()
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
root.title("Instagram Auto Poster")
root.geometry("400x250")

label_alt = tk.Label(root, text="Enter Alt Text:")
label_alt.pack()
entry_alt = tk.Entry(root, width=40)
entry_alt.pack()

label_file = tk.Label(root, text="Select Photo/Video:")
label_file.pack()
entry_file = tk.Entry(root, width=40)
entry_file.pack()
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

label_caption = tk.Label(root, text="Enter Caption:")
label_caption.pack()
entry_caption = tk.Entry(root, width=40)
entry_caption.pack()

label_location = tk.Label(root, text="Enter Location:")
label_location.pack()
entry_location = tk.Entry(root, width=40)
entry_location.pack()

button_post = tk.Button(root, text="Post to Instagram", command=on_button_click)
button_post.pack(pady=10)

label_status = tk.Label(root, text="Status: Idle")
label_status.pack(pady=10)

root.mainloop()
