from flask import Flask, render_template
from datetime import datetime, timedelta

# Import configurations
from config import OPENAI_CONFIG

# Import clients from integrations
from integrations.strava import StravaClient
from integrations.spotify import SpotifyClient
from integrations.chess import ChessClient
from integrations.openai import OpenAIClient

# Import template filters
from utils.filters import strftime, selecttracks

app = Flask(__name__)

# Register template filters
app.jinja_env.filters['strftime'] = strftime
app.jinja_env.filters['selecttracks'] = selecttracks

# Initialize clients
strava_client = StravaClient()
spotify_client = SpotifyClient()
chess_client = ChessClient()
openai_client = OpenAIClient()

@app.route("/")
def index():
    # Get data from all integrations
    activities = strava_client.get_activities()
    tracks = spotify_client.get_recent_tracks()
    
    # Group tracks by playlist: If a track has a 'playlist' context, group it under that playlist name.
    playlist_groups = {}
    non_playlist_tracks = []
    for track in tracks:
        context = track.get('context')
        if context and context.get('type') == 'playlist':
            playlist_name = spotify_client.get_playlist_name(track)
            if not playlist_name:
                playlist_name = "Unknown Playlist"
            if playlist_name not in playlist_groups:
                playlist_groups[playlist_name] = []
            playlist_groups[playlist_name].append(track)
        else:
            non_playlist_tracks.append(track)
    
    # Generate AI workout summary with included duration information
    workout_prompt = f"""
    Analyze these recent activities and provide a summary:
    
    Activities:
    {[{
        'name': activity.get('name'),
        'type': activity.get('type'),
        'distance': activity.get('distance'),
        'start_date': activity.get('start_date'),
        'duration': activity.get('elapsed_time')
    } for activity in activities]}
    
    Recent tracks played during workouts:
    {[{
        'name': track.get('name'),
        'artist': track.get('artist')
    } for track in tracks]}
    
    Please provide a brief, encouraging summary of the workout activities and music choices.
    """
    ai_summary = openai_client.generate_completion(workout_prompt)
    
    # Get chess data
    chess_profile, chess_stats = chess_client.get_profile()
    chess_games = chess_client.get_recent_games()
    chess_analysis = chess_client.analyze_games(openai_client.client, chess_games)

    return render_template(
        "index.html",
        activities=activities,
        tracks=tracks,
        playlist_groups=playlist_groups,
        non_playlist_tracks=non_playlist_tracks,
        ai_summary=ai_summary,
        chess_profile=chess_profile,
        chess_stats=chess_stats,
        chess_games=chess_games[:8],
        chess_analysis=chess_analysis
    )

if __name__ == "__main__":
    app.run(debug=True)

