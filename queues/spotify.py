import requests
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from .models import User

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

class SpotifyClient:
    def __init__(self, user:User):
        self.user = user
        self.access_token = user.access_token
        self.refresh_token()

    def refresh_token(self):
        if self.user.expiration_time <= now():
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.user.refresh_token,
                "client_id": settings.SPOTIFY_CLIENT_ID,
                "client_secret": settings.SPOTIFY_CLIENT_SECRET,
            }

            response = requests.post(SPOTIFY_TOKEN_URL, data=data)
            if response.status_code != 200:
                raise Exception("Failed to refresh token")
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")  
            self.user.access_token = self.access_token
            expiration_time = token_data.get("expires_in", 3600)
            self.user.token_expires = now() + timedelta(seconds=expiration_time)

            self.user.save()

    def get(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"https://api.spotify.com/v1/{endpoint}"
        return requests.get(url, headers=headers, params=params)
    
    def post(self, endpoint, data=None, params=None):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        url = f"https://api.spotify.com/v1/{endpoint}"
        return requests.post(url, headers=headers, json=data, params=params)