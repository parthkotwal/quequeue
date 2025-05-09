from flask import request, redirect, session, url_for, Blueprint
import config
import urllib.parse
import requests

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
    
    # Currently Playing
    output = []
    now = queue_data.get("currently_playing")
    if now:
        song = now.get("name")
        artist = now.get("artists", [{}])[0].get("name")
        output.append(f"Currently Playing: “{song}” by {artist}")
    else:
        output.append("No song currently playing.")

    # Queue

    
