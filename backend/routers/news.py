from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..utils.db import get_connection

router = APIRouter()

@router.get("/", summary="Список новостей")
def list_news(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество новостей на странице"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    card_type: Optional[str] = Query(None, description="Фильтр по типу карточки (regular/feature)")
):
    """
    Получить список новостей с пагинацией и фильтрацией
    """
    if page < 1 or limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * limit
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Базовый запрос
            query = """
                SELECT id, url, title, image, category, date, comments_count, card_type, parsed_at
                FROM news 
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
            
            # Добавляем сортировку и пагинацию
            query += " ORDER BY parsed_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # Выполняем запрос
            cur.execute(query, params)
            rows = cur.fetchall()
            
            # Преобразуем результат в словари
            news_data = []
            for row in rows:
                news_data.append({
                    "id": row[0],
                    "url": row[1],
                    "title": row[2],
                    "image": row[3],
                    "category": row[4],
                    "date": row[5],
                    "comments_count": row[6],
                    "card_type": row[7],
                    "parsed_at": row[8].isoformat() if row[8] else None
                })
            
            # Получаем общее количество новостей для пагинации
            count_query = "SELECT COUNT(*) FROM news WHERE 1=1"
            count_params = []
            
            if category:
                count_query += " AND category = %s"
                count_params.append(category)
            
            if card_type:
                count_query += " AND card_type = %s"
                count_params.append(card_type)
            
            cur.execute(count_query, count_params)
            total_count = cur.fetchone()[0]
            
            return {
                "news": news_data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения новостей: {str(e)}")

@router.get("/categories", summary="Список категорий новостей")
def get_news_categories():
    """
    Получить список всех категорий новостей
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT DISTINCT category FROM news WHERE category IS NOT NULL ORDER BY category")
            categories = [row[0] for row in cur.fetchall()]
            
            return {"categories": categories}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения категорий: {str(e)}")

@router.get("/stats", summary="Статистика новостей")
def get_news_stats():
    """
    Получить статистику по новостям
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Общее количество новостей
            cur.execute("SELECT COUNT(*) FROM news")
            total_news = cur.fetchone()[0]
            
            # Количество по категориям
            cur.execute("SELECT category, COUNT(*) FROM news WHERE category IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC")
            categories_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            # Количество по типам карточек
            cur.execute("SELECT card_type, COUNT(*) FROM news WHERE card_type IS NOT NULL GROUP BY card_type")
            card_types_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            return {
                "total_news": total_news,
                "categories": categories_stats,
                "card_types": card_types_stats
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

@router.get("/{news_id}", summary="Получить новость по ID")
def get_news_by_id(news_id: int):
    """
    Получить новость по ID
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT id, url, title, image, category, date, comments_count, card_type, parsed_at
                FROM news 
                WHERE id = %s
                """,
                (news_id,)
            )
            row = cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Новость не найдена")
            
            return {
                "id": row[0],
                "url": row[1],
                "title": row[2],
                "image": row[3],
                "category": row[4],
                "date": row[5],
                "comments_count": row[6],
                "card_type": row[7],
                "parsed_at": row[8].isoformat() if row[8] else None
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения новости: {str(e)}")
