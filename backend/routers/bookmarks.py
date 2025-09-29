from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..utils.db import get_connection
from ..utils.auth import get_current_user_id


router = APIRouter()


@router.get("/", summary="Список закладок пользователя")
def list_bookmarks(
    page: int = 1, 
    page_size: int = 20, 
    user_id: int = Depends(get_current_user_id)
):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * page_size
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT f.id, f.kinopoisk_id, f.title, f.poster, f.rating_kp, b.created_at
                FROM bookmarks b
                JOIN films f ON f.id = b.film_id
                WHERE b.user_id = %s
                ORDER BY b.created_at DESC
                LIMIT %s OFFSET %s
                """,
                (user_id, page_size, offset)
            )
            rows = cur.fetchall()
            items = [
                {
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "title": r[2],
                    "poster": r[3],
                    "rating_kp": r[4],
                    "bookmarked_at": r[5].isoformat() if r[5] else None,
                }
                for r in rows
            ]
            return {"items": items, "page": page, "page_size": page_size}
        finally:
            cur.close()


@router.post("/{film_id}", summary="Добавить фильм в закладки")
def add_bookmark(film_id: int, user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что фильм существует
            cur.execute("SELECT id FROM films WHERE id = %s", (film_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Film not found")
            
            # Добавляем закладку (ON CONFLICT игнорируем дубликаты)
            cur.execute(
                """
                INSERT INTO bookmarks (film_id, user_id) 
                VALUES (%s, %s) 
                ON CONFLICT (film_id, user_id) DO NOTHING
                RETURNING id
                """,
                (film_id, user_id)
            )
            
            result = cur.fetchone()
            if result:
                conn.commit()
                return {"status": "added", "bookmark_id": result[0]}
            else:
                return {"status": "already_exists"}
        finally:
            cur.close()


@router.delete("/{film_id}", summary="Удалить фильм из закладок")
def remove_bookmark(film_id: int, user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM bookmarks WHERE film_id = %s AND user_id = %s",
                (film_id, user_id)
            )
            conn.commit()
            
            if cur.rowcount > 0:
                return {"status": "removed"}
            else:
                return {"status": "not_found"}
        finally:
            cur.close()


@router.get("/{film_id}/status", summary="Проверить статус закладки")
def check_bookmark_status(film_id: int, user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id, created_at FROM bookmarks WHERE film_id = %s AND user_id = %s",
                (film_id, user_id)
            )
            result = cur.fetchone()
            
            if result:
                return {
                    "is_bookmarked": True,
                    "bookmark_id": result[0],
                    "bookmarked_at": result[1].isoformat() if result[1] else None
                }
            else:
                return {"is_bookmarked": False}
        finally:
            cur.close()
