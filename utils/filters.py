from datetime import datetime, timedelta

def strftime(date_str, fmt='%Y-%m-%d %H:%M:%S'):
    """Convert ISO date string to formatted date string."""
    date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    native = date.astimezone()
    return native.strftime(fmt)

def selecttracks(tracks, activity_start, activity_duration):
    """Select tracks that were played during an activity."""
    activity_start = datetime.fromisoformat(activity_start.replace('Z', '+00:00'))
    activity_end = activity_start + timedelta(seconds=activity_duration)
    
    matching_tracks = []
    for track in tracks:
        track_time = datetime.fromisoformat(track['played_at'].replace('Z', '+00:00'))
        if activity_start <= track_time <= activity_end:
            matching_tracks.append(track)
    return matching_tracks