from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..utils.auth import get_current_user_id
from ..utils.db import get_connection

router = APIRouter()


@router.post("/films/{film_id}/visit", summary="Добавить фильм в историю посещений")
def add_film_to_history(film_id: int, user_id: int = Depends(get_current_user_id)):
    """Добавляет фильм в историю посещений пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, существует ли фильм
            cur.execute("SELECT id FROM film WHERE id = %s", (film_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Фильм не найден")
            
            # Добавляем или обновляем запись в истории
            cur.execute(
                """
                INSERT INTO user_film_history (user_id, film_id, visited_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id, film_id)
                DO UPDATE SET visited_at = CURRENT_TIMESTAMP
                """,
                (user_id, film_id)
            )
            
            # Удаляем старые записи, оставляя только последние 10
            cur.execute(
                """
                DELETE FROM user_film_history
                WHERE user_id = %s AND id NOT IN (
                    SELECT id FROM user_film_history
                    WHERE user_id = %s
                    ORDER BY visited_at DESC
                    LIMIT 10
                )
                """,
                (user_id, user_id)
            )
            
            conn.commit()
            return {"message": "Фильм добавлен в историю посещений"}
            
        except HTTPException:
            raise
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка при добавлении в историю: {str(e)}")
        finally:
            cur.close()


@router.get("/films/history", summary="Получить историю посещений пользователя")
def get_user_film_history(
    user_id: int = Depends(get_current_user_id),
    limit: int = 10
):
    """Получает историю посещений фильмов пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT 
                    h.visited_at,
                    f.id,
                    f.kinopoisk_id,
                    f.title,
                    f.original_title,
                    f.poster,
                    f.year,
                    f.rating_kp,
                    f.rating_imdb
                FROM user_film_history h
                JOIN film f ON h.film_id = f.id
                WHERE h.user_id = %s
                ORDER BY h.visited_at DESC
                LIMIT %s
                """,
                (user_id, limit)
            )
            
            history = []
            for row in cur.fetchall():
                history.append({
                    "visited_at": row[0],
                    "film": {
                        "id": row[1],
                        "kinopoisk_id": row[2],
                        "title": row[3],
                        "original_title": row[4],
                        "poster": row[5],
                        "year": row[6],
                        "rating_kp": float(row[7]) if row[7] else None,
                        "rating_imdb": float(row[8]) if row[8] else None,
                    }
                })
            
            return {"history": history, "total": len(history)}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при получении истории: {str(e)}")
        finally:
            cur.close()


@router.delete("/films/history", summary="Очистить историю посещений")
def clear_user_film_history(user_id: int = Depends(get_current_user_id)):
    """Очищает всю историю посещений пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM user_film_history WHERE user_id = %s",
                (user_id,)
            )
            conn.commit()
            
            return {"message": "История посещений очищена"}
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка при очистке истории: {str(e)}")
        finally:
            cur.close()


@router.delete("/films/{film_id}/history", summary="Удалить фильм из истории посещений")
def remove_film_from_history(film_id: int, user_id: int = Depends(get_current_user_id)):
    """Удаляет конкретный фильм из истории посещений пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM user_film_history WHERE user_id = %s AND film_id = %s",
                (user_id, film_id)
            )
            conn.commit()
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Фильм не найден в истории")
            
            return {"message": "Фильм удален из истории посещений"}
            
        except HTTPException:
            raise
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка при удалении из истории: {str(e)}")
        finally:
            cur.close()


@router.get("/films/history/stats", summary="Статистика истории посещений")
def get_history_stats(user_id: int = Depends(get_current_user_id)):
    """Получает статистику истории посещений пользователя"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Общее количество посещений
            cur.execute(
                "SELECT COUNT(*) FROM user_film_history WHERE user_id = %s",
                (user_id,)
            )
            total_visits = cur.fetchone()[0]
            
            # Посещения за последние 7 дней
            cur.execute(
                """
                SELECT COUNT(*) FROM user_film_history 
                WHERE user_id = %s AND visited_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
                """,
                (user_id,)
            )
            visits_7d = cur.fetchone()[0]
            
            # Посещения за последние 30 дней
            cur.execute(
                """
                SELECT COUNT(*) FROM user_film_history 
                WHERE user_id = %s AND visited_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
                """,
                (user_id,)
            )
            visits_30d = cur.fetchone()[0]
            
            # Самый популярный жанр в истории
            cur.execute(
                """
                SELECT g.name, COUNT(*) as count
                FROM user_film_history h
                JOIN film f ON h.film_id = f.id
                JOIN film_genre fg ON f.id = fg.film_id
                JOIN genre g ON fg.genre_id = g.id
                WHERE h.user_id = %s
                GROUP BY g.name
                ORDER BY count DESC
                LIMIT 1
                """,
                (user_id,)
            )
            favorite_genre = cur.fetchone()
            
            return {
                "total_visits": total_visits,
                "visits_7d": visits_7d,
                "visits_30d": visits_30d,
                "favorite_genre": favorite_genre[0] if favorite_genre else None,
                "favorite_genre_count": favorite_genre[1] if favorite_genre else 0
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при получении статистики: {str(e)}")
        finally:
            cur.close()
