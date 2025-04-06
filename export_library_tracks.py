"""
Script: export_library_tracks.py

Description:
    This script fetches all the songs currently saved in your YouTube Music library
    and writes the full track details to a JSON file named 'library_tracks.json'.

Usage:
    - Ensure you are authenticated with YTMusic using a valid `browser.json` file.
    - Run the script directly. It will fetch all library songs and store them
      in a structured JSON file for reference or further processing.

Dependencies:
    - ytmusicapi
    - json (standard library)

Output:
    - A file named 'LibraryTracks.json' containing metadata for all tracks in your library.

"""

import json
import os

from ytmusicapi import YTMusic

ytmusic = YTMusic("browser.json")

tracks = ytmusic.get_library_songs(limit=2000)

output_dir = "export_files"
os.makedirs(output_dir, exist_ok=True)
filename = os.path.join(output_dir, "LibraryTracks.json")

print(f"[INFO] Writing library tracks to '{filename}'...")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(tracks, f, indent=4)

print(f"[SUCCESS] Finished writing to '{filename}'")

i = 1
for track in tracks:
    print(f"{i}. {track['title']}")
    i += 1

print(f"There are a total of {len(tracks)} songs!")
