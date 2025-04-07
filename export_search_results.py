from ytmusicapi import YTMusic
import json

print("Initializing YouTube Music API...")
ytmusic = YTMusic("browser.json")

print("Loading Spotify songs data...")
with open("transformed_spotify_saved_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

songs = data["songs"]
count = data["total_tracks"]
print(f"Found {count} songs to search")

print("\nStarting YouTube Music search...")
items = []

for i, song in enumerate(songs, 1):
    query = f"{song["name"]} - {song["artists"]}"
    print(f"Searching for: {query}")
    
    results = ytmusic.search(query, filter="songs", limit=30)
    item = {
        "spotify": song,
        "ytm_matches": results
    }
    items.append(item)

print(f"\nSearch complete! Found matches for {len(items)} songs")

print("\nSaving search results to search_results.json...")
with open("search_results.json", "w", encoding="utf-8") as file:
    json.dump(items, file, indent=4, ensure_ascii=False)
print("Done!")


