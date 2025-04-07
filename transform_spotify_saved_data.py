import json

print("Loading saved tracks from spotify_saved_tracks.json...")
with open("spotify_saved_tracks.json", "r", encoding="utf-8") as file:
    data = json.load(file)

items = data["spotify_saved_tracks"]
print(f"Found {len(items)} saved tracks")

print("\nProcessing tracks to extract song information...")
tracks = [item["track"] for item in items]
songs = []

for i, track in enumerate(tracks, 1):
    id = track["id"]
    name = track["name"]
    artists = ", ".join([artist["name"]for artist in track["artists"]])
    song = {
        "spotify_id": id,
        "name": name,
        "artists": artists,
    }
    songs.append(song)


print(f"\nSuccessfully processed {len(songs)} tracks")

print("\nWriting simplified song list to temp.json...")
with open("transformed_spotify_saved_data.json", "w", encoding="utf-8") as file:
    json.dump({"songs": songs, "total_tracks": len(songs)}, file, indent=4)
print("Done!")