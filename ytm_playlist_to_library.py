"""
YouTube Music Playlist To Library Transfer Script

This script connects to YouTube Music using the ytmusicapi and performs the following actions:
1. Retrieves all tracks from a specified playlist.
2. Searches for each track in YouTube Music using the track title and artist(s).
3. If an exact match (based on videoId) is found, adds the song to the user's library.
4. Upon successful addition, marks the track for removal from the playlist.
5. After processing all tracks, removes the successfully added tracks from the playlist.

Logs:
- All actions are logged both to the console and to a uniquely timestamped log file.
- Log messages include progress tracking, success, failure, and detailed warnings or errors.

Requirements:
- `ytmusicapi` library
- A valid `browser.json` authentication file for YouTube Music (exported using ytmusicapi tools)

Usage:
- Update the `playlist_id` variable with the ID of the playlist to be cleaned up.
- Run the script.

"""

import logging
from datetime import datetime

from ytmusicapi import YTMusic

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"playlist_cleanup_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

log = logging.getLogger(__name__)
ytmusic = YTMusic("browser.json")

playlist_id = "" # Add your playlist ID here
log.info(f"Fetching playlist details for '{playlist_id}'...")
playlist_details = ytmusic.get_playlist(playlistId=playlist_id, limit=None)

tracks = playlist_details["tracks"]
log.info(f"Retrieved {len(tracks)} tracks from playlist: '{playlist_details['title']}'")
playlist_items = []

for index, track in enumerate(tracks, start=1):
    title = track.get("title")
    if not title:
        log.warning(f"[{index}/{len(tracks)}] Track is missing title. Skipping.")
        continue

    artists = track.get("artists")
    query = title
    if artists:
        artist_names = " & ".join([a.get("name", "").strip() for a in artists])
        query = f"{title} - {artist_names}"

    log.info(f"[{index}/{len(tracks)}] Processing QUERY: '{query}'...")

    get_result = ytmusic.search(query=query, filter="songs", limit=50)
    found = False

    for result in get_result:
        if result["videoId"] == track["videoId"]:
            log.info(
                f"    Found exact match for '{title}' (videoId: {result['videoId']})"
            )
            out = ytmusic.edit_song_library_status(result["feedbackTokens"]["add"])

            try:
                is_success = (
                    out.get("feedbackResponses", [{}])[0].get("isProcessed") is True
                    and out.get("actions", [{}])[0]
                    .get("addToToastAction", {})
                    .get("item", {})
                    .get("notificationActionRenderer", {})
                    .get("responseText", {})
                    .get("runs", [{}])[0]
                    .get("text")
                    == "Added to library"
                )
            except Exception as e:
                is_success = False
                log.error(f"    Exception while checking success status: {e}")

            if is_success:
                playlist_items.append(track)
                log.info(
                    f"    [SUCCESS] Added '{title}' to library. Marked for removal."
                )
            else:
                log.warning(
                    f"    Failed to confirm addition of '{title}' to library. Skipping."
                )

            found = True
            break

    if not found:
        log.warning(
            f"    Could not find matching result for '{title}' in search results."
        )

log.info(
    f"\nRemoving {len(playlist_items)} tracks from playlist '{playlist_details['title']}'..."
)
ytmusic.remove_playlist_items(playlist_id, playlist_items)
log.info("Playlist cleanup complete.")
