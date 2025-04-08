import os
import sys
import requests
from yt_dlp import YoutubeDL

# Step 1: Ask for playlist URL
playlist_url = input("🔗 Paste your YouTube playlist link here: ").strip()

# Step 2: Check if link is accessible
try:
    response = requests.get(playlist_url)
    if response.status_code != 200:
        raise Exception(f"Received status code: {response.status_code}")
    print("✅ Playlist is accessible.\n")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Step 3: Create download folder
folder_name = "Downloaded Playlist"
os.makedirs(folder_name, exist_ok=True)

# Step 4: Download using yt-dlp Python API
print(f"⬇️ Downloading videos to '{folder_name}'...\n")

ydl_opts = {
    'outtmpl': os.path.join(folder_name, '%(title)s.%(ext)s'),
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'merge_output_format': 'mp4',
    'noplaylist': False,
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])

print("\n✅ Done. Videos are in the 'Downloaded Playlist' folder.")
