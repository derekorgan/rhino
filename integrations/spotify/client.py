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
            if results is None:
                print("No results returned from Spotify API")
                return []
            return [format_track_data(item) for item in results['items']]
        except Exception as e:
            print(f"Error getting recent tracks: {e}")
            return []

    def get_playlist_name(self, track):
        """
        Given a track from the recently played tracks, this function checks if the track 
        has a context of type 'playlist' and, if so, retrieves the playlist name by calling
        the Spotify API.
        """
        context = track.get('context')
        if context and context.get('type') == 'playlist':
            playlist_uri = context.get('uri')  # e.g., "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd"
            playlist_id = playlist_uri.split(":")[-1]
            # Assuming spotify_client has a method to get a playlist's details:
            playlist_details = self.get_playlist(playlist_id)
            return playlist_details.get('name')
        return None