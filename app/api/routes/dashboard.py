from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.config import get_settings

router = APIRouter()
templates = Jinja2Templates(directory=get_settings().TEMPLATES_DIR)

@router.get("/")
async def dashboard(request: Request):
    """Main dashboard endpoint"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "activities": [],
            "tracks": [],
            "ai_summary": "Dashboard coming soon!"
        }
    )
