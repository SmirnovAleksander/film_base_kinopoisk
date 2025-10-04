from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from ..utils.db import get_connection
from ..utils.auth import get_current_user_id

router = APIRouter()


def update_film_user_rating(film_id: int):
    """Обновляет средний пользовательский рейтинг фильма в таблице film"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Вычисляем средний рейтинг и количество оценок
            cur.execute(
                """
                SELECT AVG(rating), COUNT(*)
                FROM user_film_ratings 
                WHERE film_id = %s
                """,
                (film_id,)
            )
            
            result = cur.fetchone()
            avg_rating = result[0]
            rating_count = result[1]
            
            # Обновляем таблицу film
            cur.execute(
                """
                UPDATE film 
                SET user_rating = %s, user_rating_count = %s
                WHERE id = %s
                """,
                (avg_rating, rating_count, film_id)
            )
            
            conn.commit()
            
        finally:
            cur.close()


@router.get("/films/{film_id}/rating", summary="Получить рейтинг пользователя для фильма")
def get_user_film_rating(film_id: int, user_id: int = Depends(get_current_user_id)):
    """Получает рейтинг текущего пользователя для указанного фильма"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что фильм существует
            cur.execute("SELECT id FROM film WHERE id = %s", (film_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Film not found")
            
            # Получаем рейтинг пользователя
            cur.execute(
                """
                SELECT rating, created_at, updated_at 
                FROM user_film_ratings 
                WHERE user_id = %s AND film_id = %s
                """,
                (user_id, film_id)
            )
            result = cur.fetchone()
            
            if result:
                return {
                    "rating": float(result[0]),
                    "created_at": result[1],
                    "updated_at": result[2]
                }
            else:
                return {"rating": None}
                
        finally:
            cur.close()


@router.post("/films/{film_id}/rating", summary="Установить рейтинг пользователя для фильма")
def set_user_film_rating(film_id: int, rating: float, user_id: int = Depends(get_current_user_id)):
    """Устанавливает или обновляет рейтинг текущего пользователя для указанного фильма"""
    if not (1.0 <= rating <= 10.0):
        raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 10.0")
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что фильм существует
            cur.execute("SELECT id FROM film WHERE id = %s", (film_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Film not found")
            
            # Вставляем или обновляем рейтинг
            cur.execute(
                """
                INSERT INTO user_film_ratings (user_id, film_id, rating)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, film_id) 
                DO UPDATE SET 
                    rating = EXCLUDED.rating,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING rating, created_at, updated_at
                """,
                (user_id, film_id, rating)
            )
            
            result = cur.fetchone()
            conn.commit()
            
            # Обновляем средний рейтинг фильма
            update_film_user_rating(film_id)
            
            return {
                "rating": float(result[0]),
                "created_at": result[1],
                "updated_at": result[2]
            }
                
        finally:
            cur.close()


@router.put("/films/{film_id}/rating", summary="Изменить рейтинг пользователя для фильма")
def update_user_film_rating(film_id: int, rating: float, user_id: int = Depends(get_current_user_id)):
    """Изменяет рейтинг текущего пользователя для указанного фильма"""
    if not (1.0 <= rating <= 10.0):
        raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 10.0")
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что фильм существует
            cur.execute("SELECT id FROM film WHERE id = %s", (film_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Film not found")
            
            # Проверяем, что рейтинг пользователя существует
            cur.execute(
                "SELECT id FROM user_film_ratings WHERE user_id = %s AND film_id = %s",
                (user_id, film_id)
            )
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="User rating not found. Use POST to create a new rating.")
            
            # Обновляем рейтинг
            cur.execute(
                """
                UPDATE user_film_ratings 
                SET rating = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND film_id = %s
                RETURNING rating, created_at, updated_at
                """,
                (rating, user_id, film_id)
            )
            
            result = cur.fetchone()
            conn.commit()
            
            # Обновляем средний рейтинг фильма
            update_film_user_rating(film_id)
            
            return {
                "rating": float(result[0]),
                "created_at": result[1],
                "updated_at": result[2]
            }
                
        finally:
            cur.close()


@router.delete("/films/{film_id}/rating", summary="Удалить рейтинг пользователя для фильма")
def delete_user_film_rating(film_id: int, user_id: int = Depends(get_current_user_id)):
    """Удаляет рейтинг текущего пользователя для указанного фильма"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM user_film_ratings WHERE user_id = %s AND film_id = %s",
                (user_id, film_id)
            )
            
            if cur.rowcount > 0:
                conn.commit()
                # Обновляем средний рейтинг фильма
                update_film_user_rating(film_id)
                return {"message": "Rating deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Rating not found")
                
        finally:
            cur.close()


@router.get("/films/{film_id}/rating/average", summary="Получить средний рейтинг фильма от пользователей")
def get_film_average_rating(film_id: int):
    """Получает средний рейтинг фильма от всех пользователей"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что фильм существует
            cur.execute("SELECT id FROM film WHERE id = %s", (film_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Film not found")
            
            # Получаем статистику рейтингов
            cur.execute(
                """
                SELECT 
                    AVG(rating) as average_rating,
                    COUNT(*) as total_ratings,
                    MIN(rating) as min_rating,
                    MAX(rating) as max_rating
                FROM user_film_ratings 
                WHERE film_id = %s
                """,
                (film_id,)
            )
            
            result = cur.fetchone()
            
            if result[1] > 0:  # Если есть рейтинги
                return {
                    "average_rating": round(float(result[0]), 2),
                    "total_ratings": result[1],
                    "min_rating": float(result[2]),
                    "max_rating": float(result[3])
                }
            else:
                return {
                    "average_rating": None,
                    "total_ratings": 0,
                    "min_rating": None,
                    "max_rating": None
                }
                
        finally:
            cur.close()


@router.get("/users/{user_id}/ratings", summary="Получить все рейтинги пользователя")
def get_user_ratings(user_id: int, page: int = 1, page_size: int = 20):
    """Получает все рейтинги указанного пользователя с пагинацией"""
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * page_size
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что пользователь существует
            cur.execute("SELECT id FROM app_user WHERE id = %s", (user_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="User not found")
            
            # Получаем рейтинги с информацией о фильмах
            cur.execute(
                """
                SELECT 
                    ufr.rating,
                    ufr.created_at,
                    ufr.updated_at,
                    f.id as film_id,
                    f.title,
                    f.poster,
                    f.year
                FROM user_film_ratings ufr
                JOIN film f ON ufr.film_id = f.id
                WHERE ufr.user_id = %s
                ORDER BY ufr.updated_at DESC
                LIMIT %s OFFSET %s
                """,
                (user_id, page_size, offset)
            )
            
            rows = cur.fetchall()
            ratings = []
            
            for row in rows:
                ratings.append({
                    "rating": float(row[0]),
                    "created_at": row[1],
                    "updated_at": row[2],
                    "film": {
                        "id": row[3],
                        "title": row[4],
                        "poster": row[5],
                        "year": row[6]
                    }
                })
            
            return {
                "items": ratings,
                "page": page,
                "page_size": page_size
            }
                
        finally:
            cur.close()
