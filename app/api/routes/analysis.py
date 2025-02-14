from fastapi import APIRouter
from app.models.schemas import AnalysisResponse

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/workout", response_model=AnalysisResponse)
async def analyze_workout():
    """Placeholder for workout analysis endpoint"""
    return AnalysisResponse(
        analysis="Analysis coming soon!",
        source_data={
            "activities": [],
            "tracks": []
        }
    )
