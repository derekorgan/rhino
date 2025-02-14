from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import requests
from app.core.config import get_settings
from datetime import datetime, timezone
import pytz

class StravaActivity(BaseModel):
    """Pydantic model for Strava activity data"""
    name: str
    type: str
    distance: float
    moving_time: int
    elapsed_time: int
    start_date: datetime
    average_speed: float
    has_heartrate: bool
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[float] = None
    kudos_count: int = 0
    
    @property
    def formatted_distance(self) -> str:
        """Return distance in km with 2 decimal places"""
        return f"{self.distance / 1000:.2f} km"
    
    @property
    def formatted_duration(self) -> str:
        """Return duration in human readable format"""
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m {seconds}s"
    
    @property
    def formatted_heartrate(self) -> Optional[str]:
        """Return formatted heart rate string if available"""
        if self.has_heartrate and self.average_heartrate and self.max_heartrate:
            return f"❤️ {int(self.average_heartrate)} bpm (max {int(self.max_heartrate)})"
        return None
    
    @property
    def formatted_date(self) -> str:
        """Return human readable date and time"""
        now = datetime.now(timezone.utc)
        activity_date = self.start_date.replace(tzinfo=timezone.utc)
        diff = now - activity_date
        
        # If it's today
        if diff.days == 0:
            if diff.seconds < 3600:  # Less than an hour ago
                minutes = diff.seconds // 60
                return f"{minutes} minutes ago"
            else:
                return f"Today at {activity_date.strftime('%-I:%M %p')}"
        
        # If it's yesterday
        elif diff.days == 1:
            return f"Yesterday at {activity_date.strftime('%-I:%M %p')}"
        
        # If it's within the last week
        elif diff.days < 7:
            return activity_date.strftime('%A at %-I:%M %p')  # e.g., "Tuesday at 2:30 PM"
        
        # If it's within this year
        elif activity_date.year == now.year:
            return activity_date.strftime('%b %-d at %-I:%M %p')  # e.g., "Feb 15 at 2:30 PM"
        
        # If it's older
        return activity_date.strftime('%b %-d, %Y at %-I:%M %p')  # e.g., "Feb 15, 2023 at 2:30 PM"

    @property
    def formatted_kudos(self) -> Optional[str]:
        """Return formatted kudos string if there are any"""
        if self.kudos_count > 0:
            return f"👍 {self.kudos_count}"
        return None

class StravaService:
    """Service for interacting with Strava API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client_id = self.settings.STRAVA_CLIENT_ID
        self.client_secret = self.settings.STRAVA_CLIENT_SECRET
        self.refresh_token = self.settings.STRAVA_REFRESH_TOKEN
        self.access_token = None
    
    async def _get_access_token(self) -> str:
        """Get a new access token using the refresh token"""
        response = requests.post(
            'https://www.strava.com/oauth/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.refresh_token,
                'grant_type': 'refresh_token'
            }
        )
        response.raise_for_status()
        return response.json()['access_token']
    
    async def get_activities(self, limit: int = 8) -> List[StravaActivity]:
        """Fetch recent activities from Strava"""
        if not self.access_token:
            self.access_token = await self._get_access_token()
        
        response = requests.get(
            f'https://www.strava.com/api/v3/athlete/activities',
            headers={'Authorization': f'Bearer {self.access_token}'},
            params={'per_page': limit}
        )
        response.raise_for_status()
        
        activities = []
        for activity in response.json():
            activities.append(
                StravaActivity(
                    name=activity['name'],
                    type=activity['type'],
                    distance=activity['distance'],
                    moving_time=activity['moving_time'],
                    elapsed_time=activity['elapsed_time'],
                    start_date=activity['start_date'],
                    average_speed=activity['average_speed'],
                    has_heartrate=activity['has_heartrate'],
                    average_heartrate=activity.get('average_heartrate'),
                    max_heartrate=activity.get('max_heartrate'),
                    kudos_count=activity.get('kudos_count', 0)
                )
            )
        
        return activities

    async def get_raw_activity_data(self, limit: int = 1) -> dict:
        """Debug method to print full activity response"""
        if not self.access_token:
            self.access_token = await self._get_access_token()
        
        response = requests.get(
            f'https://www.strava.com/api/v3/athlete/activities',
            headers={'Authorization': f'Bearer {self.access_token}'},
            params={'per_page': limit}
        )
        response.raise_for_status()
        
        return response.json()[0]  # Return first activity as example

    async def get_athlete_details(self) -> dict:
        """Fetch detailed athlete information"""
        if not self.access_token:
            self.access_token = await self._get_access_token()
        
        response = requests.get(
            'https://www.strava.com/api/v3/athlete',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        response.raise_for_status()
        return response.json()
