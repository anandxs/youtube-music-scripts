import base64
import json
import os
import random
import string
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request


load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

app = Flask(__name__)


def generate_random_string(length=16):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@app.route("/")
def redirect_to_login():
    return redirect("/login")


@app.route("/login")
def login():
    state = generate_random_string(16)
    scope = "user-library-read user-library-modify"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
        "state": state,
    }

    return redirect("https://accounts.spotify.com/authorize?" + urlencode(params))


@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    if state is None:
        params = {"error": "state_mismatch"}
        return redirect("/#" + urlencode(params))

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}",
    }
    data = {
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )

    with open("token.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)

    return response.json()


if __name__ == "__main__":
    app.run(port=3000, debug=True)
