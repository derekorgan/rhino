from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application settings using Pydantic"""
    APP_NAME: str = "Rhino Dashboard"
    DEBUG: bool = False
    
    # API Keys and Credentials
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    STRAVA_REFRESH_TOKEN: Optional[str] = None
    
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: Optional[str] = None
    
    OPENAI_API_KEY: str
    
    # Chess.com settings
    CHESS_USERNAME: Optional[str] = None
    
    # Withings settings
    WITHINGS_CLIENT_ID: Optional[str] = None
    WITHINGS_CLIENT_SECRET: Optional[str] = None
    WITHINGS_REDIRECT_URI: Optional[str] = None
    WITHINGS_REFRESH_TOKEN: Optional[str] = None
    
    # Optional Redis configuration for memory
    REDIS_URL: Optional[str] = None
    
    # Templates directory
    TEMPLATES_DIR: str = "app/templates"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # This will allow extra fields in the environment without raising errors

@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
