import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import get_settings
from app.api.routes import dashboard, analysis

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Mount static files - make sure the directory exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# Include routers
app.include_router(dashboard.router)
app.include_router(analysis.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 