import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Instant Media Streamer & Downloader"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database & Redis
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://streamer:streamer_pass@localhost:5432/streamer_db"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Metadata APIs
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "")
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    JIKAN_BASE_URL: str = "https://api.jikan.moe/v4"
    
    # Telegram Streamer
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_API_ID: int = int(os.getenv("TELEGRAM_API_ID", "0"))
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH", "")
    TELEGRAM_STREAM_CHANNEL_ID: str = os.getenv("TELEGRAM_STREAM_CHANNEL_ID", "")
    
    # Cache TTL (seconds)
    CACHE_EXPIRATION_SECONDS: int = 86400  # 24 Hours

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
