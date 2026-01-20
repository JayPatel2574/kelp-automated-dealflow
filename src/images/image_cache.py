from pathlib import Path
import hashlib
import requests


CACHE_DIR = Path("data/image_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cache_image(url: str) -> Path:
    """
    Downloads and caches an image locally.
    """
    name = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    path = CACHE_DIR / name

    if not path.exists():
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        path.write_bytes(r.content)

    return path
