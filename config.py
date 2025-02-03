import os
from dotenv import load_dotenv

load_dotenv()

# Strava Configuration
STRAVA_CONFIG = {
    "client_id": os.getenv("STRAVA_CLIENT_ID"),
    "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
    "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
}

# Spotify Configuration
SPOTIFY_CONFIG = {
    "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
    "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
}

# Chess.com Configuration
CHESS_CONFIG = {
    "username": os.getenv("CHESS_USERNAME", "default_username"),
}

# OpenAI Configuration
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
} 