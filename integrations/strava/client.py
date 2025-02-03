import requests
from config import STRAVA_CONFIG

class StravaClient:
    TOKEN_URL = "https://www.strava.com/oauth/token"
    API_BASE = "https://www.strava.com/api/v3"

    def __init__(self):
        self.client_id = STRAVA_CONFIG["client_id"]
        self.client_secret = STRAVA_CONFIG["client_secret"]
        self.refresh_token = STRAVA_CONFIG["refresh_token"]

    def get_access_token(self):
        response = requests.post(
            self.TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
        )
        return response.json().get("access_token")

    def get_activities(self, limit=5):
        access_token = self.get_access_token()
        if not access_token:
            return []

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{self.API_BASE}/athlete/activities",
            headers=headers,
            params={"per_page": limit}
        )
        return response.json() 