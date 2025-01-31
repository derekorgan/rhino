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

 # ✅ chess.com API
 # Load Chess.com username from .env
CHESS_USERNAME = os.getenv("CHESS_USERNAME", "default_username")

CHESS_API_BASE = f"https://api.chess.com/pub/player/{CHESS_USERNAME}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Function to fetch Chess.com profile & stats
def get_chess_profile():
    profile_url = CHESS_API_BASE
    stats_url = f"{CHESS_API_BASE}/stats"

    profile_response = requests.get(profile_url, headers=HEADERS)
    stats_response = requests.get(stats_url, headers=HEADERS)

    profile_data = profile_response.json() if profile_response.status_code == 200 else {}
    stats_data = stats_response.json() if stats_response.status_code == 200 else {}

    return profile_data, stats_data

# Function to fetch recent chess games
def get_recent_chess_games():
    archives_url = f"{CHESS_API_BASE}/games/archives"
    response = requests.get(archives_url, headers=HEADERS)

    if response.status_code == 200:
        archives = response.json().get("archives", [])
        if archives:
            latest_archive_url = archives[-1]  # Most recent month
            games_response = requests.get(latest_archive_url, headers=HEADERS)
            return games_response.json().get("games", []) if games_response.status_code == 200 else []
    
    return []

# Function to analyze recent chess games using OpenAI
def analyze_chess_games(games):
    if not games:
        return "No recent games available for analysis."

    # Extract the last 5 games summary
    game_summaries = []
    for game in games[:5]:  # Analyze last 5 games
        time_control = game.get("time_class", "Unknown").capitalize()
        white_player = game.get("white", {}).get("username", "Unknown")
        black_player = game.get("black", {}).get("username", "Unknown")
        result = game.get("white", {}).get("result", "Unknown")

        game_summaries.append(f"{time_control} | {white_player} vs {black_player} | Result: {result}")

    prompt = f"""
    I have played the following recent chess games:
    {json.dumps(game_summaries, indent=4)}

    Please analyze my performance and suggest areas for improvement.
    """

    try:
        response = openai_client.chat.completions.create(
            model="o1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating chess insights: {str(e)}"


@app.route("/")
def index():
    activities = get_latest_activities()
    tracks = get_recent_tracks()
    ai_summary = generate_workout_summary(activities, tracks)

    # ✅ Fetch Chess.com data
    chess_profile, chess_stats = get_chess_profile()
    chess_games = get_recent_chess_games()
    chess_analysis = analyze_chess_games(chess_games)


    return render_template(
        "index.html", 
        activities=activities, 
        tracks=tracks, ai_summary=ai_summary,
        chess_profile=chess_profile,  
        chess_stats=chess_stats,  
        chess_games=chess_games[:8],  
        chess_analysis=chess_analysis  
    )

if __name__ == "__main__":
    app.run(debug=True)
