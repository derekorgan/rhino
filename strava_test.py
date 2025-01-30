import requests
import os
import json

# Load Strava credentials from environment variables
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# Strava Token URL
TOKEN_URL = "https://www.strava.com/oauth/token"

# Get a new access token
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

# Fetch Strava profile data
def get_strava_profile():
    access_token = get_access_token()
    if not access_token:
        return "Failed to retrieve access token"

    headers = {"Authorization": f"Bearer {access_token}"}
    profile_url = "https://www.strava.com/api/v3/athlete"

    response = requests.get(profile_url, headers=headers)
    return response.json()

# Run test
if __name__ == "__main__":
    profile_data = get_strava_profile()
    print(json.dumps(profile_data, indent=4)) 