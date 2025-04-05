import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from io import BytesIO
from PIL import Image, ImageTk

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


# Function to Display Selected Article Details
def show_article_details(event):
    global selected_article
    selected_index = listbox.curselection()
    if not selected_index:
        return

    index = selected_index[0]
    selected_article = articles[index]

    title_label.config(text=selected_article["title"])
    short_desc_label.config(text=selected_article["shortDescription"])

    # Load and display image
    try:
        image_url = selected_article.get("images", "")
        if image_url:
            image_response = requests.get(image_url)
            image_data = Image.open(BytesIO(image_response.content))
            image_data = image_data.resize(
                (200, 150), Image.Resampling.LANCZOS
            )  # Bigger image
            img = ImageTk.PhotoImage(image_data)
            image_label.config(image=img)
            image_label.image = img
    except Exception as e:
        print(f"Error loading image: {e}")
        image_label.config(image="")


# Function to Post Article on Medium
def post_article():
    global selected_article
    if not selected_article["title"]:
        print("No article selected!")
        return
    print(
        f"Posting: {selected_article['title']}"
    )  # Backend function will handle posting


# Create Tkinter UI
root = tk.Tk()
root.title("Article Selector")
root.geometry("700x500")
root.configure(bg="#1e1e1e")  # Dark mode background

# Apply ttk theme for a modern look
style = ttk.Style()
style.theme_use("clam")

# Frame for Listbox and Scrollbar
frame = ttk.Frame(root)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

listbox = tk.Listbox(
    frame, width=50, height=10, bg="#252526", fg="white", font=("Arial", 12)
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Populate listbox
for article in articles:
    listbox.insert(tk.END, article["title"])

listbox.bind("<<ListboxSelect>>", show_article_details)

# Title Label
title_label = ttk.Label(
    root,
    text="Select an Article",
    font=("Arial", 16, "bold"),
    background="#1e1e1e",
    foreground="white",
)
title_label.pack(pady=10)

# Image Label
image_label = ttk.Label(root, background="#1e1e1e")
image_label.pack(pady=10)

# Short Description Label
short_desc_label = ttk.Label(
    root,
    text="",
    wraplength=600,
    justify="left",
    font=("Arial", 12),
    background="#1e1e1e",
    foreground="white",
)
short_desc_label.pack(pady=5)

# Post Button
post_button = ttk.Button(
    root, text="Post on Medium", command=post_article, style="TButton"
)
post_button.pack(pady=20)

# Run the Tkinter loop
root.mainloop()
