import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Load Strava credentials from environment variables
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")


TOKEN_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

# Get a fresh access token
def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "refresh_token": STRAVA_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )
    response_json = response.json()
    return response_json.get("access_token")

# Fetch latest activities
def get_latest_activities(limit=5):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to retrieve access token"}

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(ACTIVITIES_URL, headers=headers, params={"per_page": limit})
    
    activities = response.json()
    return activities

# Run test
if __name__ == "__main__":
    activities = get_latest_activities(limit=5)  # Fetch last 5 activities
    print(json.dumps(activities, indent=4))  # Pretty print JSON