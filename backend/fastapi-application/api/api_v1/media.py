from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct

from core.models import ( 
    db_helper, 
    Media
)
from core.schemas import (
    MediaRead,
    MediaResponse,
    MediaCategoriesResponse,
    MediaTypesResponse,
    MediaStatsResponse,
)

router = APIRouter(
    prefix="/media",
    tags=["Media"],
)


# GET /api/v1/media/ - Получить список всех новостей, статей и обзоров
@router.get("/", response_model=MediaResponse, summary="Список медиа контента")
async def list_media(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество элементов на странице"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    card_type: Optional[str] = Query(None, description="Фильтр по типу карточки"),
    content_type: Optional[str] = Query(None, description="Фильтр по типу контента"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список медиа контента с пагинацией и фильтрацией"""
    if page < 1 or limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * limit
    
    # Базовый запрос
    stmt = select(Media)
    conditions = []
    
    # Добавляем фильтры
    if category:
        conditions.append(Media.category == category)
    
    if card_type:
        conditions.append(Media.card_type == card_type)
    
    if content_type:
        conditions.append(Media.type == content_type)
    
    # Применяем условия
    if conditions:
        stmt = stmt.where(*conditions)
    
    # Добавляем сортировку и пагинацию
    stmt = stmt.order_by(Media.parsed_at.desc()).offset(offset).limit(limit)
    
    # Выполняем запрос
    result = await session.execute(stmt)
    media_items = result.scalars().all()
    
    # Получаем общее количество элементов для пагинации
    count_stmt = select(func.count(Media.id))
    if conditions:
        count_stmt = count_stmt.where(*conditions)
    
    count_result = await session.execute(count_stmt)
    total_count = count_result.scalar()
    
    return MediaResponse(
        media=[MediaRead.model_validate(item) for item in media_items],
        pagination={
            "page": page,
            "limit": limit,
            "total": total_count or 0,
            "pages": (total_count + limit - 1) // limit if total_count else 0,
        }
    )


# GET /api/v1/media/categories - Список уникальных категорий (например: Новости, Интервью)
@router.get("/categories", response_model=MediaCategoriesResponse, summary="Список категорий медиа")
async def get_media_categories(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить список всех категорий медиа контента"""
    stmt = (
        select(distinct(Media.category))
        .where(Media.category.is_not(None))
        .order_by(Media.category)
    )
    result = await session.execute(stmt)
    categories = [row[0] for row in result.all()]
    
    return MediaCategoriesResponse(categories=categories)


# GET /api/v1/media/types - Список типов медиа контента (news, article и т.д.)
@router.get("/types", response_model=MediaTypesResponse, summary="Список типов медиа")
async def get_media_types(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить список всех типов медиа контента"""
    stmt = (
        select(distinct(Media.type))
        .where(Media.type.is_not(None))
        .order_by(Media.type)
    )
    result = await session.execute(stmt)
    types = [row[0] for row in result.all()]
    
    return MediaTypesResponse(types=types)


# GET /api/v1/media/stats - Статистическая информация по общему количеству и распределению медиа
@router.get("/stats", response_model=MediaStatsResponse, summary="Статистика медиа")
async def get_media_stats(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить статистику по медиа контенту"""
    # Общее количество медиа контента
    total_stmt = select(func.count(Media.id))
    total_result = await session.execute(total_stmt)
    total_media = total_result.scalar()
    
    # Количество по категориям
    categories_stmt = (
        select(Media.category, func.count(Media.id))
        .where(Media.category.is_not(None))
        .group_by(Media.category)
        .order_by(func.count(Media.id).desc())
    )
    categories_result = await session.execute(categories_stmt)
    categories_stats = {row[0]: row[1] for row in categories_result.all()}
    
    # Количество по типам карточек
    card_types_stmt = (
        select(Media.card_type, func.count(Media.id))
        .where(Media.card_type.is_not(None))
        .group_by(Media.card_type)
    )
    card_types_result = await session.execute(card_types_stmt)
    card_types_stats = {row[0]: row[1] for row in card_types_result.all()}
    
    # Количество по типам контента
    content_types_stmt = (
        select(Media.type, func.count(Media.id))
        .where(Media.type.is_not(None))
        .group_by(Media.type)
        .order_by(func.count(Media.id).desc())
    )
    content_types_result = await session.execute(content_types_stmt)
    content_types_stats = {row[0]: row[1] for row in content_types_result.all()}
    
    return MediaStatsResponse(
        total_media=total_media or 0,
        categories=categories_stats,
        card_types=card_types_stats,
        content_types=content_types_stats,
    )


# GET /api/v1/media/1 - Получить детальное описание конкретной новости или статьи по ID
@router.get("/{media_id}", response_model=MediaRead, summary="Получить медиа по ID")
async def get_media_by_id(
    media_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить медиа контент по ID"""
    stmt = select(Media).where(Media.id == media_id)
    result = await session.execute(stmt)
    media_item = result.scalar_one_or_none()
    
    if not media_item:
        raise HTTPException(status_code=404, detail="Медиа контент не найден")
    
    return MediaRead.model_validate(media_item)
