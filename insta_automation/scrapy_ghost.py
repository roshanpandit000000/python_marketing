import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# username = "ridhaavtrenddz"
# password = "Google@ccount@123!@#"


def stop_scraping():
    global stop_flag
    stop_flag = True
    label_status.config(text="Status: Stopping... ⏹️")
    root.update_idletasks()
    print("🛑 Stop button clicked! Attempting to stop...")


stop_flag = False


def on_button_click():
    global stop_flag
    stop_flag = False
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    tag = entry_tag.get()

    if not username or not password or not tag:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Start the scraping process in a separate thread
    thread = threading.Thread(
        target=automate_instagram_sraper, args=(username, password, tag)
    )
    thread.start()

    label_status.config(text="Status: Running ⏳")
    root.update_idletasks()


def stop_scraping():
    global stop_flag
    stop_flag = True
    label_status.config(text="Status: Stopping... ⏹️")
    root.update_idletasks()
    print("🛑 Stop button clicked! Attempting to stop...")


# Initialize Chrome WebDriver (Browser remains open after script finishes)
def automate_instagram_sraper(username, password, tag):
    global stop_flag
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    # Open Instagram login page
    driver.get("https://www.instagram.com/")
    wait = WebDriverWait(driver, 15)

    # Login Process
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)
    # Wait for homepage to load
    wait.until(EC.url_contains("instagram.com"))

    # Pause for UI stability
    time.sleep(5)

    print("Logged in successfully")

    driver.refresh()
    time.sleep(5)

    # Click the "Explore" button

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

    time.sleep(4)

    # Click the first post
    try:
        click_first_post = wait.until(
            EC.element_to_be_clickable((By.XPATH, '(//a[contains(@href, "/p/")])[1]'))
        )
        click_first_post.click()
        print("Post button clicked successfully!")
    except Exception as e:
        print(f"Failed to click the post: {e}")

    # Pause to ensure content loads
    time.sleep(5)

    # Extract and save <h3> data (repeatedly clicks 'Load more comments')
    post_count = 0
    file_path = "h3_data.html"
    # all_h3_data = []

    while True:
        if stop_flag:
            print("🛑 Scraping stopped by user (outer loop).")
            label_status.config(text="Status: Stopped ⏹️")
            root.update_idletasks()
            break
        print(f"🔍 Extracting data from post #{post_count + 1}...")

        all_comments_data = []  # Collect comments for current post

        while True:
            if stop_flag:
                print("🛑 Scraping stopped by user (inner loop).")
                label_status.config(text="Status: Stopped ⏹️")
                root.update_idletasks()
                break

            # Extract all <h3> elements (or adjust this to comments you want)
            try:
                h3_elements = driver.find_elements(By.XPATH, "//h3")
                for element in h3_elements:
                    comment_html = element.get_attribute("outerHTML")
                    if comment_html not in all_comments_data:
                        all_comments_data.append(comment_html)

                # Try to click 'Load more comments' if it exists
                try:
                    load_more_button = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                '//*[name()="svg" and @aria-label="Load more comments"]',
                            )
                        )
                    )
                    load_more_button.click()
                    print("🟢 Clicked 'Load more comments' button successfully!")
                    time.sleep(3)  # Wait for new comments to load

                except Exception as e:
                    print(
                        "❌ No 'Load more comments' button found. Finished loading comments for this post."
                    )
                    break  # Exit inner loop when there is no more "Load more comments" button

            except Exception as e:
                print(f"⚠️ Failed to extract comments: {e}")
                break

        # After exiting the inner loop, save data for this post
        if all_comments_data:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(f"\n\n<!-- Post #{post_count + 1} -->\n\n")
                file.write("\n\n".join(all_comments_data))

            print(
                f"✅ Extracted {len(all_comments_data)} comments from post #{post_count + 1}"
            )

        else:
            print("⚠️ No comments found in this post.")

        post_count += 1
        label_post_count.config(text=f"Posts Processed: {post_count}")
        root.update_idletasks()

        if stop_flag:
            print("🛑 Scraping stopped by user before clicking next.")
            label_status.config(text="Status: Stopped ⏹️")
            root.update_idletasks()
            break

        # Try to click "Next" button to go to next post
        try:
            next_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button//*[name()='svg' and @aria-label='Next']",
                    )
                )
            )
            next_button.click()
            print("➡️ Moved to next post...")
            time.sleep(5)

        except Exception as e:
            print(f"🚫 No 'Next' button found or failed to click: {e}")
            print("🎉✅ Scraping completed successfully! No more posts to process.")
            label_status.config(text="Status: Completed ✅")
            root.update_idletasks()
            break  # End the outer loop since no next post


# Create GUI
root = tk.Tk()
root.title("Instagram Auto Commenter")
root.geometry("850x650")
root.configure(bg="#f7f7f7")

# Title
title_label = tk.Label(
    root,
    text="Instagram Sraper",
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


# Buttons
button_post = ttk.Button(root, text="Start Scraping", command=on_button_click)
button_post.pack(pady=5)

# Stop Button
button_stop = ttk.Button(root, text="Stop", command=lambda: stop_scraping())
button_stop.pack(pady=5)

# Status Labels
label_status = tk.Label(
    root, text="Status: Idle", font=("Arial", 10, "italic"), bg="#f7f7f7", fg="gray"
)
label_status.pack(pady=5)

label_post_count = tk.Label(
    root, text="Comments Posted: 0", font=("Arial", 10, "bold"), bg="#f7f7f7", fg="blue"
)
label_post_count.pack(pady=5)

root.mainloop()
