from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.core.config import get_settings
from app.services.strava import StravaService

router = APIRouter()
templates = Jinja2Templates(directory=get_settings().TEMPLATES_DIR)

async def get_strava_service():
    """Dependency injection for Strava service"""
    return StravaService()

@router.get("/")
async def dashboard(
    request: Request,
    strava_service: StravaService = Depends(get_strava_service)
):
    """Main dashboard endpoint"""
    try:
        activities = await strava_service.get_activities(limit=8)
    except Exception as e:
        print(f"Error fetching Strava activities: {e}")
        activities = []
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "activities": activities,
            "tracks": [],
            "ai_summary": "Dashboard coming soon!"
        }
    )

@router.get("/debug/strava")
async def debug_strava(
    strava_service: StravaService = Depends(get_strava_service)
):
    """Debug endpoint to view raw Strava activity data"""
    return await strava_service.get_raw_activity_data()

@router.get("/debug/strava/athlete")
async def debug_strava_athlete(
    strava_service: StravaService = Depends(get_strava_service)
):
    """Debug endpoint to view athlete data"""
    return await strava_service.get_athlete_details()
