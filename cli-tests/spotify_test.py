import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-recently-played"
))

# Fetch recently played tracks
def get_recent_tracks():
    results = sp.current_user_recently_played(limit=10)  # Fetch last 10 songs
    for track in results['items']:
        track_name = track['track']['name']
        artist = track['track']['artists'][0]['name']
        played_at = track['played_at']
        print(f"{played_at}: {track_name} - {artist}")

# Run test
if __name__ == "__main__":
    get_recent_tracks()