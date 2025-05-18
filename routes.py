from flask import request, redirect, session, url_for, Blueprint
import config
import urllib.parse
import requests
import json
from datetime import datetime
import os
import time

def init_routes(app):

    @app.route("/login")
    def login():
        # 1 - redirect user to spotify login
        scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
        auth_url = "https://accounts.spotify.com/authorize"

        params = {
            "client_id": config.SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": config.SPOTIFY_REDIRECT_URI,
            "scope": scope,
        }

        full_auth_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
        return redirect(full_auth_url)
    
    @app.route("/callback")
    def callback():
        # 2 - get authorization code from URL
        code = request.args.get("code")

        # 3 - exchange code for access token
        token_url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.SPOTIFY_REDIRECT_URI,
            "client_id": config.SPOTIFY_CLIENT_ID,
            "client_secret": config.SPOTIFY_CLIENT_SECRET,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(token_url, data=payload, headers=headers)
        token_data = response.json()

        session["access_token"] = token_data.get("access_token")
        session["refresh_token"] = token_data.get("refresh_token")

        return "Login successful! You can now access Spotify data!"
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/queue")
    def get_queue():
        access_token = session.get("access_token")
        if not access_token:
            return redirect(url_for("login"))
        
        url = "https://api.spotify.com/v1/me/player/queue"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        queue_data = response.json()
        return queue_data
        # Currently Playing
        # output = []
        # now = queue_data.get("currently_playing")
        # if now:
        #     song = now.get("name")
        #     artist = now.get("artists", [{}])[0].get("name")
        #     output.append(f"Currently Playing: “{song}” by {artist}")
        # else:
        #     output.append("No song currently playing.")

        # # Queue
        # queue = queue_data.get("queue", [])
        # if queue:
        #     output.append("\nUp Next:")
        #     for i, track in enumerate(queue, start=1):
        #         name = track.get("name")
        #         artist = track.get("artists", [{}])[0].get("name")
        #         output.append(f"{i}. “{name}” by {artist}")

        # else:
        #     output.append("No queue present.")

        # # filepath = f".json"
        # # with open() as file
        
        # return "\n".join(output)

    @app.route("/export_queue")
    def export_queue():
        access_token = session.get("access_token")
        if not access_token:
            return redirect(url_for("login"))
        
        url = "https://api.spotify.com/v1/me/player/queue"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        queue_data = response.json()

        output = {}
        # Currently Playing
        currently_playing = queue_data.get("currently_playing")
        queue = queue_data.get("queue", [])

        if currently_playing and queue:
            output['currently_playing'] = {
                "id": currently_playing.get("id"),
                "name": currently_playing.get("name"),
                "artists": [artist["name"] for artist in currently_playing.get("artists", [])],
                "images": currently_playing.get("album")["images"][0],
                "uri": currently_playing.get("uri")
            }
        
            output['queue'] = []
            for track in queue:
                output["queue"].append(
                    {
                        "id": track.get("id"),
                        "name": track.get("name"),
                        "artists": [artist["name"] for artist in track.get("artists", [])],
                        "images": track.get("album")["images"][0],
                        "uri": track.get("uri")
                    }
                )
        
        else:
            return "Need to have song playing"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exports/queue_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)

        return f"Queue exported successfully to {filename}"
    
    @app.route("/restore_queue")
    def restore_queue():
        access_token = session.get("access_token")
        if not access_token:
            return redirect(url_for("login"))
        
        filename = request.args.get("filename")
        if not filename:
            return "Filename not provided"
        
        path = os.path.join("exports", filename)
        if not os.path.exists(path):
            return f"No such file: {filename}"
        
        with open(path, "r") as f:
            queue_data = json.load(f)
        
        uris = []
        now = queue_data.get("currently_playing")
        if now:
            uris.append(now.get("uri"))

        for track in queue_data.get("queue", []):
            uris.append(track.get("uri"))

        if not uris:
            return "No URIs found in saved queue."
        
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        queue_url = "https://api.spotify.com/v1/me/player/queue"
        for uri in uris:
            requests.post(f"{queue_url}?uri={uri}", headers=headers)

        return f"Restored queue from {filename} with {len(uris)} tracks."