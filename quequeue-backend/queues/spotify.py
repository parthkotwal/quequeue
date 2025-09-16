import requests
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from .models import User

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

class SpotifyClient:
    def __init__(self, user: User):
        self.user = user
        self.access_token = user.access_token

    def ensure_token(self):
        if self.user.token_expires <= now():
            self.refresh_token()

    def refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.user.refresh_token,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }
        response = requests.post(SPOTIFY_TOKEN_URL, data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to refresh token: {response.json()}")

        token_data = response.json()
        self.access_token = token_data.get("access_token")
        self.user.access_token = self.access_token

        # Some refreshes don’t return a new refresh_token
        new_refresh = token_data.get("refresh_token")
        if new_refresh:
            self.user.refresh_token = new_refresh

        expiration_time = token_data.get("expires_in", 3600)
        self.user.token_expires = now() + timedelta(seconds=expiration_time)
        self.user.save()

    def _headers(self, content_type="application/json"):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def get(self, endpoint, params=None):
        self.ensure_token()
        url = f"https://api.spotify.com/v1/{endpoint}"
        response = requests.get(url, headers=self._headers(), params=params)
        if response.status_code == 401:  # expired mid-request
            self.refresh_token()
            response = requests.get(url, headers=self._headers(), params=params)
        return response

    def post(self, endpoint, data=None, params=None):
        self.ensure_token()
        url = f"https://api.spotify.com/v1/{endpoint}"
        response = requests.post(url, headers=self._headers(), json=data, params=params)
        if response.status_code == 401:
            self.refresh_token()
            response = requests.post(url, headers=self._headers(), json=data, params=params)
        return response

    def put(self, endpoint, data=None, params=None):
        self.ensure_token()
        url = f"https://api.spotify.com/v1/{endpoint}"
        response = requests.put(url, headers=self._headers(), json=data, params=params)
        if response.status_code == 401:
            self.refresh_token()
            response = requests.put(url, headers=self._headers(), json=data, params=params)
        return response
