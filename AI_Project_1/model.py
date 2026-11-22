"""MovieLens recommendations for a Python backend."""
from functools import lru_cache
from pathlib import Path

import numpy as np

TOP_K = 10


@lru_cache(maxsize=1)
def _load():
    with np.load(Path(__file__).with_name("movie_model.npz"), allow_pickle=False) as model:
        return dict(model)


def get_recommendations(user_id: int) -> list[int]:
    """Use a historical MovieLens user ID."""
    data = _load()
    index = np.searchsorted(data["user_ids"], user_id)
    if index < len(data["user_ids"]) and data["user_ids"][index] == user_id:
        return data["user_top"][index].tolist()
    return data["fallback"].tolist()


def _rank(movie_ids, vectors, popularity, liked, seen, weight):
    scores = popularity.copy()
    if len(liked) and weight:
        profile = vectors[liked].mean(axis=0)
        norm = np.linalg.norm(profile)
        if norm > 0:
            scores = weight * (vectors @ (profile / norm)) + (1 - weight) * popularity
    scores[seen] = -np.inf
    order = np.argsort(-scores, kind="stable")[:TOP_K]
    return movie_ids[order[np.isfinite(scores[order])]].tolist()


def get_recommendations_for_likes(liked_movie_ids: list[int]) -> list[int]:
    """Rank movies using the visitor's current likes."""
    data = _load()
    movie_ids = data["movie_ids"]
    liked_ids = sorted(set(liked_movie_ids))
    if not liked_ids:
        return []
    indices = np.searchsorted(movie_ids, liked_ids)
    if np.any(indices >= len(movie_ids)) or movie_ids[indices].tolist() != liked_ids:
        raise ValueError("Unknown MovieLens movie IDs")
    return _rank(
        movie_ids, data["vectors"], data["popularity"],
        indices, indices, float(data["weight"]),
    )
