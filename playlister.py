# playlister.py

import base64
import json
import requests as http

def get_user_id(access_token):
    url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = http.get(url, headers=headers)
    print(f"User_ID response: {response.json()}")
    return response.json().get("id")

def get_recently_played_tracks(access_token):
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = http.get(url, headers=headers)
    return response.json().get("items", [])

def get_user_playlists(access_token, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = http.get(url, headers=headers)
    return response.json().get("items", [])

def create_playlist(access_token, user_id, name="Last 50 Tracks"):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "name": name,
        "description": "Tracks played in the last 24 hours",
        "public": False
    })
    
    print(f"Creating playlist with the following details:")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    response = http.post(url, headers=headers, data=data)
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    if response.status_code != 201:
        print(f"Failed to create playlist: {response.json()}")
        return None
    
    return response.json().get("id")

def purge_playlist(access_token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "tracks": []
    })
    response = http.put(url, headers=headers, data=data)
    print(f"Purging playlist response status code: {response.status_code}")
    print(f"Purging playlist response text: {response.text}")

def add_tracks_to_playlist(access_token, playlist_id, track_uris):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "uris": track_uris
    })
    response = http.post(url, headers=headers, data=data)
    print(f"Adding tracks response status code: {response.status_code}")
    print(f"Adding tracks response text: {response.text}")

def main(access_token):
    user_id = get_user_id(access_token)
    recently_played_tracks = get_recently_played_tracks(access_token)
    track_uris = [track["track"]["uri"] for track in recently_played_tracks]
    
    playlists = get_user_playlists(access_token, user_id)
    playlist_name = "Played last 24h"
    playlist_id = None
    
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            print(f"Playlist '{playlist_name}' already exists with ID: {playlist_id}")
            break
    
    if playlist_id:
        print(f"Playlist '{playlist_name}' already exists. Purging old tracks.")
        purge_playlist(access_token, playlist_id)
    else:
        print(f"Creating new playlist '{playlist_name}'.")
        playlist_id = create_playlist(access_token, user_id, playlist_name)
    
    if playlist_id:
        add_tracks_to_playlist(access_token, playlist_id, track_uris)
        return True
    return False