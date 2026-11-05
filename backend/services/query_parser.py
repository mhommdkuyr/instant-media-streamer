import re
from typing import Optional
from backend.models import ParsedQuery

class QueryParser:
    ARABIC_SEASON_PATTERNS = [
        r"(?:الموسم|الجزء)\s*(\d+)",
        r"s(\d+)",
        r"season\s*(\d+)"
    ]
    
    ARABIC_EPISODE_PATTERNS = [
        r"(?:الحلقة|حلقة)\s*(\d+)",
        r"(?:ح)\s*(\d+)",
        r"ep(?:isode)?\s*(\d+)",
        r"e(\d+)"
    ]

    @classmethod
    def parse(cls, raw_query: str) -> ParsedQuery:
        text = raw_query.strip()
        season: Optional[int] = 1
        episode: Optional[int] = 1
        media_type = "anime" # Default heuristic

        # Detect season
        for pattern in cls.ARABIC_SEASON_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                season = int(match.group(1))
                text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
                break

        # Detect episode
        for pattern in cls.ARABIC_EPISODE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                episode = int(match.group(1))
                text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
                break

        # Remove common stop words or quality descriptors
        text = re.sub(r"(?:مترجم|كامل|مدبلج|1080p|720p|480p|fhd|hd)", "", text, flags=re.IGNORECASE).strip()
        cleaned_title = re.sub(r"\s+", " ", text).strip()

        # Simple classification: if "فيلم" or "movie" in raw query
        if re.search(r"(?:فيلم|movie)", raw_query, re.IGNORECASE):
            media_type = "movie"
            episode = None
            season = None
        elif season and season > 1 or episode and episode > 0:
            media_type = "anime" # or tv

        return ParsedQuery(
            raw_query=raw_query,
            media_type=media_type,
            title=cleaned_title or raw_query,
            season=season,
            episode=episode
        )
