import json
import logging

from datetime import datetime

import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

log_filename = f"feedback_tokens_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

with open("search_results.json", "r", encoding="utf-8") as file:
    search_data = json.load(file)

tokens = []


def generate_prompt(query, results):
    return f"""
You are given a query and a list of results.
The query is: {query} and the results are: {results}.

# Task
- You have to find the best match for the query from the results array.
- Your output should be in JSON markdown format.
- Your output object should have the following fields:
    - best_match: The entire object from the results array that matches the query the best 
    - reason: The reason you chose the best match
- If you cannot find a match, return all the same output as before but give the best_match as null and reason as "No match found"
"""


logger.info("Starting to process search results...")

for index, item in enumerate(search_data):
    logger.info(
        f"Processing item {index + 1} of {len(search_data)}: {item['spotify']['name']}"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=generate_prompt(item["spotify"]["name"], item["ytm_matches"]),
    )
    string_response = response.text
    logger.info(f"Response: \n{string_response}")
    string_response = string_response.replace("```json", "").replace("```", "").strip()

    try:
        parsed_response = json.loads(string_response)
        if parsed_response["best_match"]:
            tokens.append(
                {
                    "name": item["spotify"]["name"],
                    "aritsts": item["spotify"]["artists"],
                    "spotify_id": item["spotify"]["spotify_id"],
                    "best_match": parsed_response["best_match"],
                    "reason": parsed_response["reason"],
                    "feedback_token": parsed_response["best_match"]["feedbackTokens"][
                        "add"
                    ],
                }
            )
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON response: {e}")

    delay = 2.5 
    logger.info(f"waiting for {delay} seconds to prevent Gemini rate limits")
    time.sleep(delay)

logger.info("Finished processing search results.")

logger.info("Saving feedback tokens to feedback_tokens.json...")
with open("feedback_tokens.json", "w", encoding="utf-8") as file:
    json.dump(tokens, file, indent=4)

logger.info("Feedback tokens saved to feedback_tokens.json.")
