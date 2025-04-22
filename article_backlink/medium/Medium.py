import imaplib
import email
import re
import time
import html
import requests
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Email Credentials
EMAIL = "ridhaavhair@gmail.com"
PASSWORD = "vwuekqakqezgnrcp"

# API Endpoint for Articles
API_URL = "https://ridhaavhairstudio.in/api/article"
response = requests.get(API_URL)
data = response.json()
articles = data.get("articles", [])

selected_article = {}


def show_log_window():
    log_window = tk.Toplevel(root)
    log_window.title("Execution Log")
    log_window.geometry("600x400")

    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=70, height=20)
    log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    stop_button = ttk.Button(log_window, text="Stop", command=log_window.destroy)
    stop_button.pack(pady=5)

    return log_text


def get_medium_magic_link():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, data = mail.search(None, '(FROM "noreply@medium.com")')
        mail_ids = data[0].split()

        if not mail_ids:
            return None

        latest_email_id = mail_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        match = re.search(r"https://medium\.com/m/callback/email\?token=[^ \n]+", body)
        return html.unescape(match.group(0)) if match else None
    except:
        return None


def wait_for_link(timeout=60):
    for _ in range(timeout // 5):
        link = get_medium_magic_link()
        if link:
            return link
        time.sleep(5)
    return None


def login_to_medium(driver):
    driver.get("https://medium.com/m/signin")
    time.sleep(2)

    try:
        driver.find_element(
            By.XPATH, "//button[contains(., 'Sign in with email')]"
        ).click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(
            EMAIL + Keys.ENTER
        )
    except:
        return False

    magic_link = wait_for_link()
    if magic_link:
        driver.get(magic_link)
        time.sleep(5)
        return True
    return False


def post_article():
    global selected_article
    if not selected_article:
        return

    log_text = show_log_window()  # Open log window

    def log_message(message):
        log_text.insert(tk.END, message + "\n")
        log_text.yview(tk.END)
        root.update_idletasks()

    # driver = webdriver.Chrome(
    #     service=Service(ChromeDriverManager().install()), options=Options()
    # )

    # 🔹 Setup Selenium WebDriver
    options = Options()
    options.add_experimental_option("detach", True)  # Keep browser open after execution
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    if not login_to_medium(driver):
        driver.quit()
        return

    log_message("✅ Connected to existing Chrome session!")
    driver.get("https://medium.com")
    time.sleep(3)

    try:
        write_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Write')]")
        write_button.click()
        log_message("✅ Clicked 'Write' button")
        time.sleep(3)
    except Exception as e:
        log_message(f"❌ Error clicking 'Write' button: {e}")
        driver.quit()
        return

    article_data = {
        "title": selected_article["title"],
        "mainDescription": selected_article["mainDescription"],
        "image_url": selected_article["images"],
    }

    try:
        wait = WebDriverWait(driver, 10)
        title_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[@data-testid='editorTitleParagraph']")
            )
        )
        title_input.click()
        title_input.clear()
        title_input.send_keys(article_data["title"])
        time.sleep(5)
        driver.refresh()
        time.sleep(5)

        content_input = driver.find_element(
            By.XPATH, "(//p[@data-testid='editorParagraphText'])"
        )

        driver.execute_script(
            """
            if (arguments[0]) {
                if (arguments[1]) {
                    var img = document.createElement('img');
                    img.src = arguments[1];
                    img.style.maxWidth = '100%';
                    arguments[0].appendChild(img);
                    arguments[0].appendChild(document.createElement('br'));
                }
                arguments[0].innerHTML += arguments[2];
            }
            """,
            content_input,
            article_data["image_url"],
            article_data["mainDescription"],
        )

        time.sleep(1)
        log_message("✅ Article posted successfully!")
    except Exception as e:
        log_message(f"❌ Error posting article: {e}")
        driver.quit()
        return

    try:
        wait = WebDriverWait(driver, 10)
        publish_button = driver.find_element(
            By.XPATH, "//button[@data-action='show-prepublish']"
        )
        publish_button.click()
        time.sleep(3)
        log_message("✅ Publish button clicked successfully!")
    except Exception as e:
        log_message(f"❌ Error clicking publish button: {e}")

    try:
        wait = WebDriverWait(driver, 10)
        topics = [
            "hair",
            "beauty",
            "fashion",
            "style",
            "makeup",
            "extensions",
            "wigs",
            "salon",
        ]
        max_options = 5  # Max number of topics to add

        for index in range(min(len(topics), max_options)):
            # Re-locate the topic input each time to avoid stale element reference
            topic_input = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//p[@data-testid='editorParagraphText' and contains(span, 'Add a topic…')]",
                    )
                )
            )
            topic_input.click()
            time.sleep(1)

            # Send the topic input
            topic_input.send_keys(topics[index])
            time.sleep(1)

            # Select the first available suggestion
            first_suggestion = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//li[@data-action='typeahead-populate'])[1]")
                )
            )
            first_suggestion.click()
            time.sleep(1)

            log_message(f"✅ Added topic: {topics[index]}")

        # Click the "Publish now" button after selecting topics
        publish_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-action='publish']"))
        )
        publish_button.click()
        time.sleep(3)

        log_message("✅ Topics added and article published successfully!")

    except Exception as e:
        log_message(f"❌ Error in adding topics or publishing: {e}")


def start_posting():
    thread = threading.Thread(target=post_article)
    thread.daemon = True  # Allows program to exit even if thread is running
    thread.start()


root = tk.Tk()
root.title("Article Publisher")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame, bg="#1e1e1e")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

listbox = tk.Listbox(
    left_frame, width=40, height=15, bg="#252526", fg="white", font=("Arial", 12)
)
listbox.pack(fill=tk.BOTH, expand=True)

for article in articles:
    listbox.insert(tk.END, article["title"])


def show_article_details(event):
    global selected_article
    selected_index = listbox.curselection()
    if not selected_index:
        return
    selected_article = articles[selected_index[0]]


title_label = ttk.Label(
    main_frame,
    text="Select an Article",
    font=("Arial", 16, "bold"),
    background="#1e1e1e",
    foreground="white",
)
title_label.pack(pady=10)

post_button = ttk.Button(main_frame, text="Post on Medium", command=start_posting)
post_button.pack(pady=20)

listbox.bind("<<ListboxSelect>>", show_article_details)
root.mainloop()
