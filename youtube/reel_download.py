import os
import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)


def download_video():
    url = url_entry.get().strip()
    save_path = folder_path.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube Shorts URL.")
        return
    if not save_path:
        messagebox.showerror("Error", "Please select a folder to save the video.")
        return

    try:
        ydl_opts = {
            "outtmpl": os.path.join(save_path, "downloaded_video.%(ext)s"),
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", f"Video downloaded to:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Download Failed", str(e))


# Create GUI window
root = tk.Tk()
root.title("YouTube Shorts Downloader")
root.geometry("460x220")
root.resizable(False, False)

# URL input
tk.Label(root, text="YouTube Shorts URL:").pack(pady=(10, 0))
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Folder input
tk.Label(root, text="Save to Folder:").pack(pady=(10, 0))
folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)
folder_path = tk.StringVar(
    value=os.path.expanduser(r"~\Videos")
)  # Default to Videos folder
folder_entry = tk.Entry(folder_frame, textvariable=folder_path, width=45)
folder_entry.pack(side=tk.LEFT)
browse_btn = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_btn.pack(side=tk.LEFT, padx=5)

# Download button
download_button = tk.Button(root, text="Download as MP4", command=download_video)
download_button.pack(pady=20)

root.mainloop()
