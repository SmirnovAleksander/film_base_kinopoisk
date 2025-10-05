from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..utils.db import get_connection

router = APIRouter()

@router.get("/", summary="Список медиа контента")
def list_media(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество элементов на странице"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    card_type: Optional[str] = Query(None, description="Фильтр по типу карточки (regular/feature)"),
    content_type: Optional[str] = Query(None, description="Фильтр по типу контента (news/video/game/podcast)")
):
    """
    Получить список медиа контента с пагинацией и фильтрацией
    """
    if page < 1 or limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * limit
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Базовый запрос
            query = """
                SELECT id, url, title, image, category, date, comments_count, card_type, type, parsed_at
                FROM media 
                WHERE 1=1
            """
            params = []
            
            # Добавляем фильтры
            if category:
                query += " AND category = %s"
                params.append(category)
            
            if card_type:
                query += " AND card_type = %s"
                params.append(card_type)
            
            if content_type:
                query += " AND type = %s"
                params.append(content_type)
            
            # Добавляем сортировку и пагинацию
            query += " ORDER BY parsed_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Выполняем запрос
            cur.execute(query, params)
            rows = cur.fetchall()
            
            # Преобразуем результат в словари
            media_data = []
            for row in rows:
                media_data.append({
                    "id": row[0],
                    "url": row[1],
                    "title": row[2],
                    "image": row[3],
                    "category": row[4],
                    "date": row[5],
                    "comments_count": row[6],
                    "card_type": row[7],
                    "type": row[8],
                    "parsed_at": row[9].isoformat() if row[9] else None
                })
            
            # Получаем общее количество элементов для пагинации
            count_query = "SELECT COUNT(*) FROM media WHERE 1=1"
            count_params = []
            
            if category:
                count_query += " AND category = %s"
                count_params.append(category)
            
            if card_type:
                count_query += " AND card_type = %s"
                count_params.append(card_type)
            
            if content_type:
                count_query += " AND type = %s"
                count_params.append(content_type)
            
            cur.execute(count_query, count_params)
            total_count = cur.fetchone()[0]
            
            return {
                "media": media_data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения медиа контента: {str(e)}")

@router.get("/categories", summary="Список категорий медиа")
def get_media_categories():
    """
    Получить список всех категорий медиа контента
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT DISTINCT category FROM media WHERE category IS NOT NULL ORDER BY category")
            categories = [row[0] for row in cur.fetchall()]
            
            return {"categories": categories}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения категорий: {str(e)}")

@router.get("/types", summary="Список типов медиа")
def get_media_types():
    """
    Получить список всех типов медиа контента
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT DISTINCT type FROM media WHERE type IS NOT NULL ORDER BY type")
            types = [row[0] for row in cur.fetchall()]
            
            return {"types": types}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения типов: {str(e)}")

@router.get("/stats", summary="Статистика медиа")
def get_media_stats():
    """
    Получить статистику по медиа контенту
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Общее количество медиа контента
            cur.execute("SELECT COUNT(*) FROM media")
            total_media = cur.fetchone()[0]
            
            # Количество по категориям
            cur.execute("SELECT category, COUNT(*) FROM media WHERE category IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC")
            categories_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            # Количество по типам карточек
            cur.execute("SELECT card_type, COUNT(*) FROM media WHERE card_type IS NOT NULL GROUP BY card_type")
            card_types_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            # Количество по типам контента
            cur.execute("SELECT type, COUNT(*) FROM media WHERE type IS NOT NULL GROUP BY type ORDER BY COUNT(*) DESC")
            content_types_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            return {
                "total_media": total_media,
                "categories": categories_stats,
                "card_types": card_types_stats,
                "content_types": content_types_stats
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

@router.get("/{media_id}", summary="Получить медиа по ID")
def get_media_by_id(media_id: int):
    """
    Получить медиа контент по ID
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT id, url, title, image, category, date, comments_count, card_type, type, parsed_at
                FROM media 
                WHERE id = %s
                """,
                (media_id,)
            )
            row = cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Медиа контент не найден")
            
            return {
                "id": row[0],
                "url": row[1],
                "title": row[2],
                "image": row[3],
                "category": row[4],
                "date": row[5],
                "comments_count": row[6],
                "card_type": row[7],
                "type": row[8],
                "parsed_at": row[9].isoformat() if row[9] else None
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения медиа контента: {str(e)}")
