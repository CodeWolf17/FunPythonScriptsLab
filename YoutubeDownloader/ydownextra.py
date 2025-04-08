import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import threading
import os
from tkinter import ttk

def download_video():
    url = url_entry.get()
    output_path = folder_path.get()
    
    if not url:
        messagebox.showwarning("No URL", "Please paste a YouTube video or playlist link.")
        return
    if not output_path:
        messagebox.showwarning("No Folder", "Please choose a folder to save the videos.")
        return

    # Disable the button to prevent double clicks
    download_btn.config(state='disabled')
    status_label.config(text="⏳ Downloading... Please wait.")
    progress_bar.start()

    def run_download():
        try:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'format': 'bestvideo+bestaudio',
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_label.config(text="✅ Download complete!")
            messagebox.showinfo("Success", "Download completed successfully!")
        except Exception as e:
            status_label.config(text="❌ Failed: " + str(e))
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            download_btn.config(state='normal')
            progress_bar.stop()

    threading.Thread(target=run_download).start()

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

def toggle_dark_mode():
    if dark_mode.get():
        root.configure(bg="#2e2e2e")
        title_label.config(bg="#2e2e2e", fg="#f7f4ff")
        url_entry.config(bg="#444", fg="#fff", insertbackground="white")
        status_label.config(bg="#2e2e2e", fg="#fff")
        folder_display.config(bg="#2e2e2e", fg="#fff")
        folder_frame.config(bg="#2e2e2e")
        download_btn.config(bg="#007bff", fg="white")
        choose_btn.config(bg="#6c757d", fg="white")
        dark_mode_btn.config(bg="#6c757d", fg="white")
    else:
        root.configure(bg="#f8f9fa")
        title_label.config(bg="#f8f9fa", fg="#007bff")
        url_entry.config(bg="#ffffff", fg="#495057", insertbackground="black")
        status_label.config(bg="#f8f9fa", fg="#495057")
        folder_display.config(bg="#f8f9fa", fg="#495057")
        folder_frame.config(bg="#f8f9fa")
        download_btn.config(bg="#28a745", fg="white")
        choose_btn.config(bg="#007bff", fg="white")
        dark_mode_btn.config(bg="#f8f9fa", fg="#007bff")

# GUI setup
root = tk.Tk()
root.title("🎥 YouTube Downloader by Prof. Nhembo")
root.geometry("500x400")
root.configure(bg="#f8f9fa")

folder_path = tk.StringVar()
dark_mode = tk.BooleanVar(value=False)

# Title
title_label = tk.Label(root, text="🎬 YouTube Video / Playlist Downloader", font=("Segoe UI", 18, "bold"), bg="#f8f9fa", fg="#007bff")
title_label.pack(pady=20)

# URL Entry
url_entry = tk.Entry(root, width=50, font=("Segoe UI", 12), bd=2, relief="flat", justify="center")
url_entry.pack(pady=10)
url_entry.insert(0, "Paste your YouTube video or playlist link here...")

# Choose folder
folder_frame = tk.Frame(root, bg="#f8f9fa")
folder_frame.pack(pady=5)

choose_btn = tk.Button(folder_frame, text="📁 Choose Folder", font=("Segoe UI", 12), bg="#007bff", fg="white", relief="flat", padx=15, pady=5, command=choose_folder)
choose_btn.pack(side="left", padx=10)

folder_display = tk.Label(folder_frame, textvariable=folder_path, font=("Segoe UI", 12), bg="#f8f9fa", fg="#495057")
folder_display.pack(side="left")

# Download button
download_btn = tk.Button(root, text="⬇️ Start Download", font=("Segoe UI", 14, "bold"), bg="#28a745", fg="white", relief="flat", width=20, padx=15, pady=10, command=download_video)
download_btn.pack(pady=15)

# Progress Bar
progress_bar = ttk.Progressbar(root, length=300, mode="indeterminate")
progress_bar.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", font=("Segoe UI", 12), bg="#f8f9fa", fg="#495057")
status_label.pack()

# Dark Mode Toggle
dark_mode_btn = tk.Checkbutton(root, text="🌙 Dark Mode", variable=dark_mode, font=("Segoe UI", 12), bg="#f8f9fa", fg="#007bff", command=toggle_dark_mode)
dark_mode_btn.pack(pady=10)

# Run the GUI
root.mainloop()
