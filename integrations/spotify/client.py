import os
import requests
from datetime import datetime, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CONFIG
from .utils import format_track_data

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CONFIG["client_id"],
            client_secret=SPOTIFY_CONFIG["client_secret"],
            redirect_uri=SPOTIFY_CONFIG["redirect_uri"],
            scope="user-read-recently-played"
        ))

    def get_recent_tracks(self, limit=50):
        try:
            results = self.sp.current_user_recently_played(limit=limit)
            return [format_track_data(item) for item in results['items']]
        except Exception as e:
            print(f"Error getting recent tracks: {e}")
            return []