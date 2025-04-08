import json

from ytmusicapi import YTMusic

ytmusic = YTMusic("browser.json")

print("Loading intermediate feedback tokens...")
with open("intermediate_feedback_tokens.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Processing feedback responses...")
for item in data:
    result = ytmusic.edit_song_library_status([item["token"]])
    if (
        result.get("feedbackResponses")[0].get("isProcessed") is True
        and result.get("actions", [{}])[0]
        .get("addToToastAction", {})
        .get("item", {})
        .get("notificationActionRenderer", {})
        .get("responseText", {})
        .get("runs", [{}])[0]
        .get("text")
        == "Added to library"
    ):
        print(f"Successfully added track to YTM")
        item["status"] = "success"
    else:
        print(f"Failed to add track with id: {item['spotify_id']} to YTM")
        item["status"] = "failed"


print("Writing results to add_to_ytm_results.json...")
with open("add_to_ytm_results.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Process completed.")
