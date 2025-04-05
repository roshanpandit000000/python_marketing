import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import requests
from io import BytesIO

# API Endpoint
API_URL = "https://ridhaavhairstudio.in/api/article"

# Fetch API Data
response = requests.get(API_URL)
data = response.json()  # Convert JSON response to dictionary

articles = data.get("articles", [])  # Extract list of articles


# Function to Display Selected Article Details
def show_article_details(event):
    selected_index = listbox.curselection()  # Get selected item index
    if not selected_index:
        return

    index = selected_index[0]
    article = articles[index]

    title_label.config(text=article["title"])  # Set title
    short_desc_label.config(text=article["shortDescription"])  # Set short description

    # Set main description (Clear previous text first)
    main_desc_text.config(state=tk.NORMAL)  # Enable editing
    main_desc_text.delete("1.0", tk.END)  # Clear text area
    main_desc_text.insert(tk.END, article["mainDescription"])  # Insert new text
    main_desc_text.config(state=tk.DISABLED)  # Disable editing

    # Load and Display Article Image
    try:
        image_url = article.get("images", "")
        if image_url:
            image_response = requests.get(image_url)
            image_data = Image.open(BytesIO(image_response.content))
            image_data = image_data.resize(
                (100, 100), Image.Resampling.LANCZOS
            )  # Resize image
            img = ImageTk.PhotoImage(image_data)
            image_label.config(image=img)
            image_label.image = img  # Keep reference to prevent garbage collection
    except Exception as e:
        print(f"Error loading image: {e}")
        image_label.config(image="")  # Clear image if loading fails


# Create Tkinter Window
root = tk.Tk()
root.title("Article Selector")
root.geometry("900x700")  # Set window size

# Frame for Listbox
frame = tk.Frame(root)
frame.pack(pady=10)

# Listbox for Articles
listbox = tk.Listbox(frame, width=80, height=10)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for Listbox
scrollbar = tk.Scrollbar(frame, orient="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Populate Listbox with Titles
for article in articles:
    listbox.insert(tk.END, article["title"])

# Bind Click Event to Show Article Details
listbox.bind("<<ListboxSelect>>", show_article_details)

# Title Label
title_label = tk.Label(root, text="Select an Article", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Image Label (For Article Image)
image_label = tk.Label(root)
image_label.pack(pady=10)

# Short Description Label
short_desc_label = tk.Label(
    root, text="", wraplength=700, justify="left", font=("Arial", 12)
)
short_desc_label.pack(pady=5)

# Main Description Text Area (Scrollable)
main_desc_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
main_desc_text.pack(pady=10)
main_desc_text.config(state=tk.DISABLED)  # Initially disabled

# Run Tkinter UI
root.mainloop()
