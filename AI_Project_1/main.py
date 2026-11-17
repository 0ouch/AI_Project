from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from model import get_recommendations # Импортируем модель Участника 2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загружаем базу фильмов (от Участника 1)
print("Загрузка базы фильмов...")
movies_df = pd.read_csv('clean_movies_ui.csv')
movies_df.set_index('movieId', inplace=True)
print("База загружена!")

@app.post("/recommend/user/{user_id}")
def recommend_movies(user_id: int, liked_data: dict = Body(...)):
    # 1. Получаем лайки (пока модель их не использует, но фронт присылает)
    liked_movies = liked_data.get("liked_movie_ids", [])
    
    # 2. Спрашиваем у модели Участника 2, что посоветовать
    recommended_ids = get_recommendations(user_id)
    
    # 3. Собираем ответ с реальными картинками
    result = []
    for m_id in recommended_ids:
        if m_id in movies_df.index: # Проверка, что фильм есть в базе
            movie = movies_df.loc[m_id]
            result.append({
                "movie_id": int(m_id),
                "title": str(movie['title']),
                "poster_url": str(movie['poster_url'])
            })
            
    return {"user_id": user_id, "recommendations": result}