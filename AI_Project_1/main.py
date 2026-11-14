from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_movies = [
    {"movie_id": 1, "title": "Toy Story", "poster_url": "https://via.placeholder.com/150"},
    {"movie_id": 2, "title": "Jumanji", "poster_url": "https://via.placeholder.com/150"},
]

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int):
    return {"user_id": user_id, "recommendations": fake_movies}