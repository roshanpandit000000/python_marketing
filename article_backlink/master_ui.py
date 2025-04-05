import requests
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

# API Endpoint for Articles
API_URL = "https://ridhaavhairstudio.in/api/article"
response = requests.get(API_URL)
data = response.json()
articles = data.get("articles", [])

selected_article = {}

root = tk.Tk()  # ✅ Initialize Tkinter root first
root.title("Article Publisher")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# ✅ Now define BooleanVars after Tk() is initialized
post_medium = tk.BooleanVar()
post_linkedin = tk.BooleanVar()


def show_log_window():
    log_window = tk.Toplevel(root)
    log_window.title("Execution Log")
    log_window.geometry("600x400")

    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=70, height=20)
    log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    stop_button = ttk.Button(log_window, text="Stop", command=log_window.destroy)
    stop_button.pack(pady=5)

    return log_text


def post_medium_article(log_text):
    log_text.insert(tk.END, "Posting on Medium...\n")
    log_text.yview(tk.END)
    root.update_idletasks()


def post_on_linkedin(log_text):
    log_text.insert(tk.END, "Posting on LinkedIn...\n")
    log_text.yview(tk.END)
    root.update_idletasks()


def start_posting():
    if not selected_article:
        return

    log_text = show_log_window()

    if post_medium.get():
        thread1 = threading.Thread(target=post_medium_article, args=(log_text,))
        thread1.daemon = True
        thread1.start()

    if post_linkedin.get():
        thread2 = threading.Thread(target=post_on_linkedin, args=(log_text,))
        thread2.daemon = True
        thread2.start()


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
    title_label.config(text=f"Selected: {selected_article['title']}")


title_label = ttk.Label(
    main_frame,
    text="Select an Article",
    font=("Arial", 16, "bold"),
    background="#1e1e1e",
    foreground="white",
)
title_label.pack(pady=10)

checkbox_frame = tk.Frame(main_frame, bg="#1e1e1e")
checkbox_frame.pack(pady=10)

tk.Checkbutton(
    checkbox_frame,
    text="Post on Medium",
    variable=post_medium,
    bg="#1e1e1e",
    fg="white",
    selectcolor="#1e1e1e",
).pack(anchor="w")

tk.Checkbutton(
    checkbox_frame,
    text="Post on LinkedIn",
    variable=post_linkedin,
    bg="#1e1e1e",
    fg="white",
    selectcolor="#1e1e1e",
).pack(anchor="w")

post_button = ttk.Button(main_frame, text="Build Backlink", command=start_posting)
post_button.pack(pady=20)

listbox.bind("<<ListboxSelect>>", show_article_details)
root.mainloop()
