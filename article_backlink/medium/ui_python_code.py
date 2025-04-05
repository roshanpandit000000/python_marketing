import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

# API Endpoint
API_URL = "https://ridhaavhairstudio.in/api/article"

# Fetch API Data
response = requests.get(API_URL)
data = response.json()
articles = data.get("articles", [])

# Initialize selected article data
global selected_article
default_article = {
    "title": "",
    "shortDescription": "",
    "mainDescription": "",
    "images": "",
}
selected_article = default_article.copy()


def start_posting():
    thread = threading.Thread(target=post_article)
    thread.daemon = True  # Allows program to exit even if thread is running
    thread.start()


def show_log_window():
    log_window = tk.Toplevel(root)
    log_window.title("Execution Log")
    log_window.geometry("600x400")

    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=70, height=20)
    log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    stop_button = ttk.Button(log_window, text="Stop", command=log_window.destroy)
    stop_button.pack(pady=5)

    return log_text


# Function to Display Selected Article Details
def show_article_details(event):
    global selected_article
    selected_index = listbox.curselection()
    if not selected_index:
        return

    index = selected_index[0]
    selected_article = articles[index]

    title_label.config(text=selected_article["title"])
    # Update short description text
    short_desc_text.config(state=tk.NORMAL)
    short_desc_text.delete("1.0", tk.END)
    short_desc_text.insert(tk.END, selected_article["shortDescription"])
    short_desc_text.config(state=tk.DISABLED)

    # Load and display image
    try:
        image_url = selected_article.get("images", "")
        if image_url:
            image_response = requests.get(image_url)
            image_data = Image.open(BytesIO(image_response.content))
            image_data = image_data.resize((100, 100), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(image_data)
            image_label.config(image=img)
            image_label.image = img
    except Exception as e:
        print(f"Error loading image: {e}")
        image_label.config(image="")

# post funsion
def post_article():
    global selected_article
    if not selected_article["title"]:
        print("No article selected!")
        return

    log_text = show_log_window()  # Open log window

    def log_message(message):
        log_text.insert(tk.END, message + "\n")
        log_text.yview(tk.END)
        root.update_idletasks()

    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

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
            time.sleep(2)

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


# Create Tkinter UI
root = tk.Tk()
root.title("Article Publisher")
root.geometry("800x600")
root.configure(bg="#1e1e1e")  # Dark mode background

# Apply ttk theme for a modern look
style = ttk.Style()
style.theme_use("clam")

# Main Frame
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left Frame (Scrollable Listbox)
left_frame = tk.Frame(main_frame, bg="#1e1e1e")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

listbox_label = ttk.Label(
    left_frame,
    text="Articles",
    font=("Arial", 14, "bold"),
    background="#1e1e1e",
    foreground="white",
)
listbox_label.pack()

listbox_frame = tk.Frame(left_frame, bg="#252526")
listbox_frame.pack(fill=tk.BOTH, expand=True)

listbox_scroll = ttk.Scrollbar(listbox_frame, orient="vertical")
listbox = tk.Listbox(
    listbox_frame,
    width=40,
    height=15,
    bg="#252526",
    fg="white",
    font=("Arial", 12),
    yscrollcommand=listbox_scroll.set,
)
listbox_scroll.config(command=listbox.yview)
listbox_scroll.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Populate listbox
for article in articles:
    listbox.insert(tk.END, article["title"])

listbox.bind("<<ListboxSelect>>", show_article_details)

# Right Frame (Article Details)
right_frame = tk.Frame(main_frame, bg="#1e1e1e")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

title_label = ttk.Label(
    right_frame,
    text="Select an Article",
    font=("Arial", 16, "bold"),
    background="#1e1e1e",
    foreground="white",
)
title_label.pack(pady=10)

# Image Label
image_label = ttk.Label(right_frame, background="#1e1e1e")
image_label.pack(pady=10)

# Short Description Scrollable Textbox
desc_frame = ttk.Frame(right_frame)
desc_frame.pack(pady=5, fill=tk.BOTH, expand=True)

short_desc_text = scrolledtext.ScrolledText(
    desc_frame,
    wrap=tk.WORD,
    width=60,
    height=6,
    font=("Arial", 12),
    bg="#252526",
    fg="white",
)
short_desc_text.pack(fill=tk.BOTH, expand=True)
short_desc_text.config(state=tk.DISABLED)

# Post Button
post_button = ttk.Button(
    right_frame, text="Post on Medium", command=start_posting, style="TButton"
)
post_button.pack(pady=20)

# Run the Tkinter loop
root.mainloop()
