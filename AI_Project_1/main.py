from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from model import get_recommendations, get_recommendations_for_likes

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

movies_db = {}
with open('clean_movies_ui.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        movies_db[int(row['movieId'])] = {"title": row['title'], "poster_url": row['poster_url']}

def format_response(ids):
    return [{"movie_id": m_id, "title": movies_db[m_id]["title"], "poster_url": movies_db[m_id]["poster_url"]} for m_id in ids if m_id in movies_db]

@app.get("/recommend/{user_id}")
def recommend_by_user(user_id: int):
    return {"user_id": user_id, "recommendations": format_response(get_recommendations(user_id))}

@app.post("/recommend/likes")
def recommend_by_likes(liked_data: dict = Body(...)):
    try:
        ids = get_recommendations_for_likes(liked_data.get("liked_movie_ids", []))
    except ValueError:
        raise HTTPException(status_code=422, detail="Unknown movie IDs")
    return {"recommendations": format_response(ids)}