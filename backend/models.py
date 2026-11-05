from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MediaRecord(Base):
    __tablename__ = "media_records"

    id = Column(Integer, primary_key=True, index=True)
    canonical_id = Column(String, index=True) # e.g. tmdb_1234 or mal_99
    title = Column(String, nullable=False)
    original_title = Column(String, nullable=True)
    media_type = Column(String, index=True) # movie, tv, anime
    season_number = Column(Integer, default=1)
    episode_number = Column(Integer, default=1)
    quality = Column(String, default="1080p")
    direct_url = Column(String, nullable=False)
    telegram_file_id = Column(String, nullable=True)
    source_name = Column(String, default="auto-scraped")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_media_ep_lookup", "canonical_id", "season_number", "episode_number", "quality"),
    )

# --- Pydantic Schemas ---
class ParsedQuery(BaseModel):
    raw_query: str
    media_type: str = Field(description="anime, movie, or tv")
    title: str
    season: Optional[int] = 1
    episode: Optional[int] = 1
    quality: Optional[str] = "1080p"

class MediaItem(BaseModel):
    id: str
    title: str
    original_title: Optional[str] = None
    media_type: str
    poster_url: Optional[str] = None
    release_date: Optional[str] = None
    overview: Optional[str] = None

class StreamOption(BaseModel):
    quality: str
    direct_download_url: str
    stream_url: str
    source: str
    is_cached: bool = True
