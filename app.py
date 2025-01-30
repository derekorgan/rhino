import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import openai
from dotenv import load_dotenv  # ✅ Load environment variables

# ✅ Load .env variables
load_dotenv()

app = Flask(__name__)

# ✅ Load credentials from .env
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Configure OpenAI API key
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

TOKEN_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

# ✅ Initialize Spotify
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-recently-played"
))

# ✅ Function to refresh Strava access token
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

# ✅ Fetch latest Strava activities
def get_latest_activities(limit=5):
    access_token = get_access_token()
    if not access_token:
        return []

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(ACTIVITIES_URL, headers=headers, params={"per_page": limit})

    return response.json()

# ✅ Fetch recently played Spotify tracks
def get_recent_tracks(limit=10):
    results = sp.current_user_recently_played(limit=limit)
    tracks = []

    for item in results['items']:
        track = {
            "played_at": item['played_at'],
            "name": item['track']['name'],
            "artist": item['track']['artists'][0]['name']
        }
        tracks.append(track)

    return tracks

# ✅ OpenAI: Generate AI-powered workout summary
def generate_workout_summary(activities, tracks):
    prompt = f"""
    Here is the user's recent workout data from Strava:
    {json.dumps(activities, indent=2)}

    Here is their recently played Spotify music:
    {json.dumps(tracks, indent=2)}

    Generate a short snappy fun, engaging, and motivational summary of their workouts and music habits.
    Include:
    - How music influenced their workouts
    - Fun or inspiring trends
    - Encouragement for their next workout
    """
    try:
        response = openai_client.chat.completions.create(
            model="o1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    except Exception as e:  
        print(f"OpenAI Error: {e}")
        return "OpenAI failed to generate a response. Please check your API key or try again later."
    
@app.route("/")
def index():
    activities = get_latest_activities()
    tracks = get_recent_tracks()
    ai_summary = generate_workout_summary(activities, tracks)

    return render_template("index.html", activities=activities, tracks=tracks, ai_summary=ai_summary)

if __name__ == "__main__":
    app.run(debug=True)
