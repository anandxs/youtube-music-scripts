import json
import logging
from datetime import datetime

from ytmusicapi import YTMusic

import requests

log_filename = f"spotify_to_ytm_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

with open("token.json", "r", encoding="utf-8") as file:
    data = json.load(file)

access_token = data["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

ytmusic = YTMusic("browser.json")

spotify_songs_to_be_removed = []
next_url = "https://api.spotify.com/v1/me/tracks?limit=50"

while next_url:
    try:
        response = requests.get(next_url, headers=headers)
        response.raise_for_status()
        spotify_saved_tracks_data = response.json()

        spotify_saved_items = spotify_saved_tracks_data["items"]
        next_url = spotify_saved_tracks_data.get("next")

        for spotify_item in spotify_saved_items:
            spotify_track = spotify_item["track"]
            track_name = spotify_track["name"]
            artists_names = ", ".join(
                [artist["name"] for artist in spotify_track["artists"]]
            )
            search_query = f"{track_name} - {artists_names}"

            try:
                search_results = ytmusic.search(search_query, filter="songs", limit=50)

                found = False
                for result in search_results:
                    if (
                        result["title"] == track_name
                        and result["artists"][0]["name"] in artists_names
                    ):
                        save_result = ytmusic.edit_song_library_status(
                            result["feedbackTokens"]["add"]
                        )

                        try:
                            is_success = (
                                save_result.get("feedbackResponses", [{}])[0].get(
                                    "isProcessed"
                                )
                                is True
                                and save_result.get("actions", [{}])[0]
                                .get("addToToastAction", {})
                                .get("item", {})
                                .get("notificationActionRenderer", {})
                                .get("responseText", {})
                                .get("runs", [{}])[0]
                                .get("text")
                                == "Added to library"
                            )
                        except Exception as e:
                            logger.error(
                                f"Error checking success status for {track_name}: {str(e)}"
                            )
                            is_success = False

                        if is_success:
                            spotify_songs_to_be_removed.append(spotify_track["id"])
                            logger.info(
                                f"Successfully added {track_name} - {artists_names} to YTM"
                            )
                        else:
                            logger.warning(
                                f"Could not add {track_name} - {artists_names} to YTM"
                            )

                        found = True
                        break

                if not found:
                    logger.warning(
                        f"Could not find matching result for {track_name} - {artists_names} on YTM"
                    )
            except Exception as e:
                logger.error(f"Error processing {track_name}: {str(e)}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Spotify tracks: {str(e)}")
        break

if spotify_songs_to_be_removed:
    try:
        # Process in chunks of 50 songs as Spotify has a limit
        chunk_size = 50
        for i in range(0, len(spotify_songs_to_be_removed), chunk_size):
            chunk = spotify_songs_to_be_removed[i : i + chunk_size]
            remove_response = requests.delete(
                f"https://api.spotify.com/v1/me/tracks?ids={','.join(chunk)}",
                headers=headers,
            )
            remove_response.raise_for_status()
            logger.info(f"Successfully removed {len(chunk)} songs from Spotify")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error removing songs from Spotify: {str(e)}")
else:
    logger.info("No songs to remove from Spotify")
