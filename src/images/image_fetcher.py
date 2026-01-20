import os
import random
import requests
from typing import Optional

from src.images.image_rules import SECTOR_IMAGE_KEYWORDS, BANNED_KEYWORDS
from src.images.image_cache import cache_image


UNSPLASH_URL = "https://api.unsplash.com/search/photos"
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


class ImageFetcher:
    """
    Fetches anonymous, sector-relevant stock images.
    """

    def fetch(self, sector: str) -> Optional[str]:
        keywords = SECTOR_IMAGE_KEYWORDS.get(sector, SECTOR_IMAGE_KEYWORDS["General"])
        query = random.choice(keywords)

        if not UNSPLASH_KEY:
            print("[WARN] Unsplash key missing — skipping image fetch")
            return None

        params = {
            "query": query,
            "orientation": "landscape",
            "per_page": 5
        }
        headers = {
            "Authorization": f"Client-ID {UNSPLASH_KEY}"
        }

        r = requests.get(UNSPLASH_URL, params=params, headers=headers, timeout=10)
        r.raise_for_status()

        results = r.json().get("results", [])
        for img in results:
            alt = (img.get("alt_description") or "").lower()
            if any(bad in alt for bad in BANNED_KEYWORDS):
                continue

            url = img["urls"]["regular"]
            local_path = cache_image(url)
            return str(local_path)

        return None
