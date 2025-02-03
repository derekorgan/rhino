from datetime import datetime, timedelta

def format_track_data(track_item):
    """Format a Spotify track item into a simplified dictionary"""
    track = track_item['track']
    return {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'played_at': track_item['played_at'],
        'album': track['album']['name'],
        'duration_ms': track['duration_ms'],
        'url': track['external_urls'].get('spotify', '')
    }

def get_tracks_in_timeframe(tracks, start_time, end_time):
    """Filter tracks that were played within a specific timeframe"""
    matching_tracks = []
    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    
    for track in tracks:
        track_time = datetime.fromisoformat(track['played_at'].replace('Z', '+00:00'))
        if start_dt <= track_time <= end_dt:
            matching_tracks.append(track)
    
    return matching_tracks

def calculate_listening_time(tracks):
    """Calculate total listening time from a list of tracks"""
    total_ms = sum(track.get('duration_ms', 0) for track in tracks)
    return timedelta(milliseconds=total_ms)