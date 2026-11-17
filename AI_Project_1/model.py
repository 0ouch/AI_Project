"""MovieLens recommendations for the FastAPI backend."""

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _load_recommendations():
    path = Path(__file__).with_name("movie_recommendations.json")
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def get_recommendations(user_id: int) -> list[int]:
    """Return 10 MovieLens movie IDs in recommendation order."""
    data = _load_recommendations()
    return list(data["users"].get(str(user_id), data["fallback"]))
