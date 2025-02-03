import os
import requests
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Chess.com username from .env
CHESS_USERNAME = os.getenv("CHESS_USERNAME", "default_username")

CHESS_API_BASE = f"https://api.chess.com/pub/player/{CHESS_USERNAME}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_chess_profile():
    profile_url = CHESS_API_BASE
    stats_url = f"{CHESS_API_BASE}/stats"

    profile_response = requests.get(profile_url, headers=HEADERS)
    stats_response = requests.get(stats_url, headers=HEADERS)

    profile_data = profile_response.json() if profile_response.status_code == 200 else {}
    stats_data = stats_response.json() if stats_response.status_code == 200 else {}

    return profile_data, stats_data

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

def analyze_chess_games(openai_client, games):
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