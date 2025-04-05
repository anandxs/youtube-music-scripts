"""
Script: export_playlist.py

Description:
    This script fetches the details of a YouTube Music playlist using the YTMusic API
    and saves the response to a JSON file named after the playlist title.

Usage:
    - Make sure you have authenticated with YTMusic and have a valid `browser.json` file.
    - Replace the `playlistId` variable with the desired YouTube Music playlist ID.
    - Run the script. It will create a file named "<playlist-title>.json" containing
      the full playlist details.

Dependencies:
    - ytmusicapi
    - json (standard library)

"""

import json
import os

from ytmusicapi import YTMusic

ytmusic = YTMusic("browser.json")

playlist_details = ytmusic.get_playlist(
    playlistId="VLPLXo1SXfATCKA510jsQ_kq0jYPYi_OSMnY",  # Enter your playlist ID here. Look at the network tab for any IDs when you click on the playlist
    limit=None,
)

output_dir = "export_files"
os.makedirs(output_dir, exist_ok=True)
filename = os.path.join(output_dir, f"{playlist_details['title']}.json")

print(f"[INFO] Writing playlist details to '{filename}'...")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(playlist_details, f, indent=4)

print(f"[SUCCESS] Finished writing to '{filename}'")
