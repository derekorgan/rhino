from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Activity(BaseModel):
    name: str
    type: str
    distance: Optional[float]
    start_date: datetime
    elapsed_time: int
    
    @property
    def formatted_duration(self) -> str:
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m" if hours else f"{minutes}m {seconds}s"

class Track(BaseModel):
    name: str
    artist: str
    played_at: datetime
    playlist_name: Optional[str] = None

class AnalysisResponse(BaseModel):
    analysis: str
    source_data: Dict[str, Any]

class WorkoutPlan(BaseModel):
    title: str
    description: str
    activities: List[Dict[str, Any]]
    recommendations: List[str]
