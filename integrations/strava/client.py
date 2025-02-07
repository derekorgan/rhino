import requests
from config import STRAVA_CONFIG
from datetime import timedelta

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

    def get_activities(self, per_page=30):
        url = f"{self.API_BASE}/athlete/activities?per_page={per_page}"
        headers = {"Authorization": f"Bearer {self.get_access_token()}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            activities = response.json()
            for activity in activities:
                elapsed_time = activity.get("elapsed_time")
                if elapsed_time is not None:
                    activity["formatted_duration"] = self.humanize_duration(elapsed_time)
                else:
                    activity["formatted_duration"] = ""
            return activities
        else:
            print(f"Error fetching activities: {response.status_code} - {response.text}")
            return []

    def humanize_duration(self, seconds):
        """Convert seconds to a human-readable format."""
        total_seconds = int(seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        else:
            return f"{minutes}m {secs}s"