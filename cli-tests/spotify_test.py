import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Request extra scope to read private playlists in case the playlist is private
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-recently-played playlist-read-private"
))

def get_recent_tracks_raw(limit=2):
    """
    Fetch the raw JSON data from Spotify's Recently Played Tracks endpoint.
    """
    results = sp.current_user_recently_played(limit=limit)
    print("=== Raw JSON Response ===")
    print(json.dumps(results, indent=2))
    return results

def group_recent_tracks(limit=2):
    """
    Group recently played tracks by playlist, if a playlist context exists.
    Otherwise, add to non-playlist tracks.
    """
    results = sp.current_user_recently_played(limit=limit)
    grouped_by_playlist = {}
    non_playlist_tracks = []

    for item in results.get("items", []):
        track_info = {
            'name': item['track']['name'],
            'artist': item['track']['artists'][0]['name'],
            'played_at': item.get('played_at'),
            'context': item.get('context')
        }
        context = item.get("context")
        if context and context.get("type") == "playlist":
            playlist_uri = context.get("uri")
            if playlist_uri:
                # Extract playlist id from URI format "spotify:playlist:<playlist_id>"
                playlist_id = playlist_uri.split(":")[-1]
                try:
                    playlist_details = sp.playlist(playlist_id)
                    playlist_name = playlist_details.get("name", "Unknown Playlist")
                except Exception as e:
                    print(f"Error fetching details for playlist ID {playlist_id}: {e}")
                    playlist_name = "Unknown Playlist"
            else:
                playlist_name = "Unknown Playlist"
            if playlist_name not in grouped_by_playlist:
                grouped_by_playlist[playlist_name] = []
            grouped_by_playlist[playlist_name].append(track_info)
        else:
            non_playlist_tracks.append(track_info)

    return grouped_by_playlist, non_playlist_tracks

def print_grouped_tracks():
    """
    Print the grouped tracks to the console.
    """
    grouped_by_playlist, non_playlist_tracks = group_recent_tracks()
    
    print("\n=== Recently Played Tracks Grouped by Playlist ===")
    if grouped_by_playlist:
        for playlist_name, tracks in grouped_by_playlist.items():
            print(f"\nPlaylist: {playlist_name}")
            for t in tracks:
                context_type = t['context'].get('type') if t['context'] else 'None'
                print(f"  {t['played_at']}: {t['name']} by {t['artist']} (Context: {context_type})")
    else:
        print("No tracks with a playlist context found.")

    print("\n=== Tracks Without a Playlist Context ===")
    if non_playlist_tracks:
        for t in non_playlist_tracks:
            context_type = t['context'].get('type') if t['context'] else 'None'
            print(f"  {t['played_at']}: {t['name']} by {t['artist']} (Context: {context_type})")
    else:
        print("All tracks had a playlist context.")

if __name__ == "__main__":
    print(">>> Debug: Printing Raw Recently Played JSON")
    get_recent_tracks_raw()
    
    print("\n>>> Debug: Printing Grouping of Recently Played Tracks")
    print_grouped_tracks()