import json

import requests
from dotenv import load_dotenv

load_dotenv()

with open("token.json", "r", encoding="utf-8") as file:
    data = json.load(file)

access_token = data["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

with open("add_to_ytm_results.json", "r", encoding="utf-8") as file:
    data = json.load(file)

spotify_songs_to_be_removed = [
    item["spotify_id"] for item in data if item["status"] == "success"
]

if spotify_songs_to_be_removed:
    try:
        chunk_size = 50
        for i in range(0, len(spotify_songs_to_be_removed), chunk_size):
            chunk = spotify_songs_to_be_removed[i : i + chunk_size]
            print(f"Removing chunk of {len(chunk)} songs from Spotify...")
            remove_response = requests.delete(
                f"https://api.spotify.com/v1/me/tracks?ids={','.join(chunk)}",
                headers=headers,
            )
            remove_response.raise_for_status()
            print(f"Successfully removed {len(chunk)} songs from Spotify")
    except requests.exceptions.RequestException as e:
        print(f"Error removing songs from Spotify: {str(e)}")
else:
    print("No songs to remove from Spotify")
