import json
import requests

with open("token.json", "r", encoding="utf-8") as file:
    data = json.load(file)

access_token = data["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Collect all tracks first
all_tracks = []
next_url = "https://api.spotify.com/v1/me/tracks?limit=50"
page = 1

print("Starting to collect saved tracks...")
while next_url:
    print(f"Fetching page {page}...")
    response = requests.get(next_url, headers=headers)
    response_data = response.json()

    saved_tracks = response_data["items"]
    all_tracks.extend(saved_tracks)  # Add tracks to our collection
    next_url = response_data.get("next")
    page += 1

print(f"\nCollection complete! Found {len(all_tracks)} tracks.")

# Write all tracks as a single JSON structure
print("Writing tracks to spotify_saved_tracks.json...")
with open("spotify_saved_tracks.json", "w", encoding="utf-8") as file:
    json.dump({"spotify_saved_tracks": all_tracks}, file, indent=4)
print("Done!")
