import httpx
from typing import List, Optional
from backend.config import settings
from backend.models import MediaItem

class MetadataService:
    @staticmethod
    async def search_tmdb(query: str, media_type: str = "multi") -> List[MediaItem]:
        if not settings.TMDB_API_KEY:
            return []
        url = f"{settings.TMDB_BASE_URL}/search/{media_type}"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "query": query,
            "language": "ar"
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                return []
            results = resp.json().get("results", [])
            items = []
            for item in results[:5]:
                title = item.get("title") or item.get("name") or "Unknown"
                poster_path = item.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                items.append(MediaItem(
                    id=f"tmdb_{item.get('id')}",
                    title=title,
                    original_title=item.get("original_title") or item.get("original_name"),
                    media_type=item.get("media_type", "movie"),
                    poster_url=poster_url,
                    release_date=item.get("release_date") or item.get("first_air_date"),
                    overview=item.get("overview")
                ))
            return items

    @staticmethod
    async def search_anime_jikan(query: str) -> List[MediaItem]:
        url = f"{settings.JIKAN_BASE_URL}/anime"
        params = {"q": query, "limit": 5}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code != 200:
                    return []
                data = resp.json().get("data", [])
                items = []
                for item in data:
                    images = item.get("images", {}).get("jpg", {})
                    items.append(MediaItem(
                        id=f"mal_{item.get('mal_id')}",
                        title=item.get("title", ""),
                        original_title=item.get("title_japanese"),
                        media_type="anime",
                        poster_url=images.get("large_image_url") or images.get("image_url"),
                        release_date=item.get("aired", {}).get("string"),
                        overview=item.get("synopsis")
                    ))
                return items
        except Exception:
            return []
