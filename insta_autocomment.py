import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import traceback
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Global stop flag
stop_flag = False


def log_error(error_message):
    """Logs error messages to a file."""
    with open("error_log.txt", "a") as file:
        file.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")


def on_button_click():
    global stop_flag
    stop_flag = False
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    tag = entry_tag.get()
    comments_text = text_comments.get("1.0", tk.END).strip()

    if not username or not password or not tag or not comments_text:
        messagebox.showerror("Error", "All fields are required!")
        return

    comments_list = [c.strip() for c in comments_text.split("\n") if c.strip()]

    if not comments_list:
        messagebox.showerror("Error", "Please enter at least one valid comment!")
        return

    automate_instagram_comment(username, password, tag, comments_list)


def stop_automation():
    global stop_flag
    stop_flag = True


def automate_instagram_comment(username, password, tag, comments_list):
    global stop_flag
    label_status.config(text="Opening Instagram...")
    root.update()

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    comment_count = 0
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        wait = WebDriverWait(driver, 15)

        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        try:
            not_now_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(), 'Not now')]")
                )
            )
            not_now_button.click()
        except:
            pass

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Home')]")
            )
        )

        search_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    """/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[2]/span/div/a/div/div[1]/div""",
                )
            )
        )
        search_button.click()

        time.sleep(3)
        search_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@aria-label='Search input']")
            )
        )
        search_input.send_keys(tag)

        time.sleep(3)
        first_result = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//a[contains(@href, '/explore/tags/')])[1]")
            )
        )
        first_result.click()

        time.sleep(5)
        first_post = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(@href, '/p/')])[1]"))
        )
        first_post.click()

        time.sleep(4)
        while not stop_flag:
            existing_comment = driver.find_elements(
                By.XPATH,
                "//a[contains(@href, '/ridhaavhairstudio/') and not(contains(@class, '_a6hd'))]",
            )
            if existing_comment:
                print("Skipping post, comment already exists.")

            else:
                # Check if commenting is restricted on the post
                comment_restricted = driver.find_elements(
                    By.XPATH,
                    "//span[contains(text(), 'Comments on this post have been limited')]",
                )
                if comment_restricted:
                    print("Skipping post, comments are limited.")

                else:
                    comment_text = random.choice(comments_list)
                    wait = WebDriverWait(driver, 10)
                    comment_box = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//textarea[@aria-label='Add a comment…']")
                        )
                    )
                    comment_box.click()

                    wait = WebDriverWait(driver, 10)
                    comment_box_input = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//textarea[@aria-label='Add a comment…']")
                        )
                    )
                    comment_box_input.send_keys(comment_text)
                    time.sleep(1)
                    comment_box_input.send_keys(Keys.ENTER)
                    comment_count += 1
                    label_comment_count.config(text=f"Comments Posted: {comment_count}")
                    root.update()

            time.sleep(5)
            try:
                next_post = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button//*[name()='svg' and @aria-label='Next']")
                    )
                )
                next_post.click()
                time.sleep(2)
            except:
                break

        label_status.config(text="Automation Stopped!")
        root.update()

    except Exception as e:
        error_message = traceback.format_exc()
        log_error(error_message)
        label_status.config(text="Error occurred!")
        messagebox.showerror("Error", error_message)
    finally:
        driver.quit()


# Create GUI
root = tk.Tk()
root.title("Instagram Auto Commenter")
root.geometry("850x650")
root.configure(bg="#f7f7f7")

# Title
title_label = tk.Label(
    root,
    text="Instagram Auto Commenter",
    font=("Arial", 16, "bold"),
    bg="#f7f7f7",
    fg="#333",
)
title_label.pack(pady=10)

# Username Input
username_label = tk.Label(
    root, text="Enter your Instagram credentials:", font=("Arial", 10), bg="#f7f7f7"
)
username_label.pack(pady=5)
entry_username = ttk.Entry(root, width=30, font=("Arial", 12))
entry_username.pack(pady=5)

# Password Input
entry_password = ttk.Entry(root, width=30, font=("Arial", 12), show="*")
entry_password.pack(pady=5)

# Hashtag Input
entry_label = tk.Label(
    root,
    text="Enter the hashtag you want to comment on:",
    font=("Arial", 10),
    bg="#f7f7f7",
)
entry_label.pack(pady=5)
entry_tag = ttk.Entry(root, width=30, font=("Arial", 12))
entry_tag.pack(pady=5)

# Comments Input
text_comments = tk.Text(
    root, height=5, width=50, font=("Arial", 12), relief="solid", borderwidth=1
)
text_comments.pack(pady=5)

# Buttons
button_post = ttk.Button(root, text="Start Commenting", command=on_button_click)
button_post.pack(pady=5)

button_stop = ttk.Button(root, text="Stop", command=stop_automation)
button_stop.pack(pady=5)

# Status Labels
label_status = tk.Label(
    root, text="Status: Idle", font=("Arial", 10, "italic"), bg="#f7f7f7", fg="gray"
)
label_status.pack(pady=5)

label_comment_count = tk.Label(
    root, text="Comments Posted: 0", font=("Arial", 10, "bold"), bg="#f7f7f7", fg="blue"
)
label_comment_count.pack(pady=5)

root.mainloop()
