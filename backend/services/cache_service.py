import json
import redis.asyncio as redis
from typing import Optional, Any
from backend.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get_cached_stream(self, canonical_id: str, season: int, episode: int, quality: str) -> Optional[dict]:
        key = f"stream:{canonical_id}:s{season}:e{episode}:{quality}"
        data = await self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_cached_stream(self, canonical_id: str, season: int, episode: int, quality: str, payload: dict):
        key = f"stream:{canonical_id}:s{season}:e{episode}:{quality}"
        await self.redis_client.set(key, json.dumps(payload), ex=settings.CACHE_EXPIRATION_SECONDS)

cache_service = CacheService()
