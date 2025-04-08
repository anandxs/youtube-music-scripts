import json
import logging
from datetime import datetime

import readchar
from ytmusicapi import YTMusic

log_filename = f"spotify_to_ytm_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
ytmusic = YTMusic("browser.json")

logger.info("Starting to process feedback tokens...")
with open("feedback_tokens.json", "r", encoding="utf-8") as file:
    data = json.load(file)

feedback_tokens = []

for item in data:
    id = item["spotify_id"]
    name = item["name"]
    artists = item["aritsts"]
    reason = item["reason"]
    token = item["feedback_token"]
    result = item["best_match"]
    result_name = result["title"]
    result_artist = ", ".join([artist["name"] for artist in result["artists"]])

    print(
        f"""\nQuery: {name} by {artists}.
Match: {result_name} by {result_artist}.

Do you want to add this song to your YouTube Music library? (Press y to continue, any other key to skip)\n"""
    )

    key = readchar.readkey()
    if key.lower() == "y":
        logger.info(
            f"{result_name} by {result_artist} will be added to your YouTube music library."
        )
        feedback_tokens.append(
            {
                "token": token,
                "spotify_id": id,
            }
        )
    else:
        logger.info("Skipping this song...")


with open("intermediate_feedback_tokens.json", "w", encoding="utf-8") as file:
    json.dump(feedback_tokens, file, indent=4)
