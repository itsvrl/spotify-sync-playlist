# app.py - Application entry point

from flask import Flask, request, redirect, session, url_for
import os
import json
import base64
import requests as http
import urllib.parse
import playlister  # Import playlister module
from auth import get_authorization_url  # Import get_authorization_url from auth.py

app = Flask(__name__)
app.secret_key = '5cca5e5e-01f2-4bc5-af7f-23d77e2979ae'  # Replace with a random key
PLAYLIST_NAME = "Played last 24h"

# Load credentials from secrets.json
with open('secrets.json') as f:
    secrets = json.load(f)

CLIENT_ID = secrets["CLIENT_ID"]
CLIENT_SECRET = secrets["CLIENT_SECRET"]
REDIRECT_URI = secrets["REDIRECT_URI"]

def get_access_token(auth_code):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    response = http.post(auth_url, headers=headers, data=data)
    
    print(f"Access Token Response Status Code: {response.status_code}")
    print(f"Access Token Response Text: {response.text}")
    
    response_data = response.json()
    return response_data.get("access_token"), response_data.get("refresh_token")

def refresh_access_token(refresh_token):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = http.post(auth_url, headers=headers, data=data)
    
    print(f"Refresh Token Response Status Code: {response.status_code}")
    print(f"Refresh Token Response Text: {response.text}")
    
    response_data = response.json()
    return response_data.get("access_token")

@app.route('/')
def index():
    return redirect(get_authorization_url())

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if auth_code:
        access_token, refresh_token = get_access_token(auth_code)
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        return "Authorization successful. You can close this window."
    else:
        return "Authorization failed."

@app.route('/playlist')
def update_playlist():
    access_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    
    if not access_token or not refresh_token:
        return redirect(get_authorization_url())
    
    # Optionally, you can check if the access token is expired and refresh it
    # For simplicity, we will always refresh the access token here
    access_token = refresh_access_token(refresh_token)
    session['access_token'] = access_token
    
    playlist_updated = playlister.main(access_token)
    if playlist_updated:
        return "Playlist updated successfully. You can close this window."
    else:
        return "Playlist update failed."

if __name__ == '__main__':
    app.run(debug=True, port=8888)
