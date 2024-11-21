import os
import json
import base64
import urllib.parse

# Load credentials from secrets.json
with open('secrets.json') as f:
    secrets = json.load(f)

CLIENT_ID = secrets["CLIENT_ID"]
CLIENT_SECRET = secrets["CLIENT_SECRET"]
REDIRECT_URI = secrets["REDIRECT_URI"]
USERNAME = secrets["USERNAME"]

def get_authorization_url():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "playlist-modify-private user-read-private user-read-recently-played"
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return url

print("Go to the following URL to authorize the application:")
print(get_authorization_url())