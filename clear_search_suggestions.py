"""
remove_search_suggestions.py

This script removes all YouTube Music search suggestions associated with the authenticated account.

It uses the YTMusic API to:
1. Fetch current search suggestions using `get_search_suggestions`.
2. Remove the suggestions using `remove_search_suggestions`.
3. Repeat the process until no more suggestions remain.

This is useful for cleaning up stale or irrelevant search history from your YouTube Music profile.

Requirements:
- You must be authenticated via a valid `browser.json` file.
- `ytmusicapi` must be installed: pip install ytmusicapi

"""

from ytmusicapi import YTMusic

ytmusic = YTMusic("browser.json")

print("[INFO] Fetching initial search suggestions...")
search_results = ytmusic.get_search_suggestions(query="", detailed_runs=True)

iteration = 1
total_removed = 0

while len(search_results) > 0:
    print(
        f"[INFO] Iteration {iteration}: Found {len(search_results)} suggestions to remove."
    )

    out = ytmusic.remove_search_suggestions(search_results)
    if out:
        print(f"[SUCCESS] Removed {len(search_results)} search suggestions.")
        total_removed += len(search_results)
    else:
        print("[WARNING] Failed to remove suggestions or nothing was removed.")

    print("[INFO] Fetching remaining search suggestions...")
    search_results = ytmusic.get_search_suggestions(query="", detailed_runs=True)
    iteration += 1

print(f"[DONE] Finished. Total suggestions removed: {total_removed}")
