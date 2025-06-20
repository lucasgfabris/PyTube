import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from dotenv import load_dotenv

ENV_PATH = ".env"

# Load environment variables
def set_env_variable(key, value):
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break

    if not found:
        lines.append(f"{key}={value}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    os.environ[key] = value

def download_playlist():
    url = entry_url.get().strip()
    path = entry_path.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter the playlist link.")
        return
    if not path:
        messagebox.showerror("Error", "Please enter the destination folder path.")
        return

    set_env_variable("DOWNLOAD_PATH", path)
    os.makedirs(path, exist_ok=True)

    try:
        command = [
            "yt-dlp.exe",
            "-x",
            "--audio-format", "mp3",
            "-o", os.path.join(path, "%(title)s.%(ext)s"),
            url
        ]

        subprocess.run(command, check=True)
        messagebox.showinfo("Completed", "Playlist download completed!")

    except subprocess.CalledProcessError as e:
        error_file = os.path.join(path, "errors.txt")
        with open(error_file, "a", encoding="utf-8") as f:
            f.write(url + "\n")
        messagebox.showerror("Error", f"Error downloading the playlist:\n{e}")

# GUI
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("600x200")

label_url = tk.Label(root, text="YouTube playlist link:")
label_url.pack(pady=(10, 0))

entry_url = tk.Entry(root, width=80)
entry_url.pack()

label_path = tk.Label(root, text="Destination folder path:")
label_path.pack(pady=(10, 0))

default_path = os.getenv("DOWNLOAD_PATH", "")
entry_path = tk.Entry(root, width=80)
entry_path.insert(0, default_path)
entry_path.pack()

download_button = tk.Button(root, text="Download Playlist", command=download_playlist)
download_button.pack(pady=15)

root.mainloop()