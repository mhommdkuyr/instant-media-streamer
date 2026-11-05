from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from backend.config import settings
from backend.database import get_db, init_db
from backend.models import ParsedQuery, MediaItem, StreamOption, MediaRecord
from backend.services.query_parser import QueryParser
from backend.services.metadata_service import MetadataService
from backend.services.cache_service import cache_service
from backend.services.stream_fetcher import StreamFetcher

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for instant movie and anime search, metadata lookup, and streaming."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
    except Exception as e:
        print(f"Database init skipped or pending connection: {e}")

@app.get("/")
def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs": "/docs"
    }

@app.get(f"{settings.API_V1_PREFIX}/parse", response_model=ParsedQuery)
def parse_query(q: str = Query(..., description="Arabic or English search prompt")):
    return QueryParser.parse(q)

@app.get(f"{settings.API_V1_PREFIX}/search", response_model=List[MediaItem])
async def search_media(q: str = Query(...)):
    parsed = QueryParser.parse(q)
    results: List[MediaItem] = []
    
    # Query anime or movies/tv
    if parsed.media_type == "anime":
        results = await MetadataService.search_anime_jikan(parsed.title)
    
    if not results:
        results = await MetadataService.search_tmdb(parsed.title, media_type="multi")
        
    return results

@app.get(f"{settings.API_V1_PREFIX}/stream/{{canonical_id}}", response_model=List[StreamOption])
async def get_stream_options(
    canonical_id: str,
    season: int = 1,
    episode: int = 1,
    quality: str = "1080p",
    db: AsyncSession = Depends(get_db)
):
    # 1. Check Redis Cache
    cached = await cache_service.get_cached_stream(canonical_id, season, episode, quality)
    if cached:
        return cached

    # 2. Check Database
    stmt = select(MediaRecord).where(
        MediaRecord.canonical_id == canonical_id,
        MediaRecord.season_number == season,
        MediaRecord.episode_number == episode
    )
    result = await db.execute(stmt)
    record = result.scalars().first()
    telegram_file_id = record.telegram_file_id if record else None

    # 3. Resolve Streams
    options = await StreamFetcher.resolve_streams(
        canonical_id=canonical_id,
        season=season,
        episode=episode,
        telegram_file_id=telegram_file_id
    )

    # 4. Cache in Redis
    await cache_service.set_cached_stream(
        canonical_id, season, episode, quality, [opt.model_dump() for opt in options]
    )

    return options
