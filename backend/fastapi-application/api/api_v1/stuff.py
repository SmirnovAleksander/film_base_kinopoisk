from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.models import ( 
    db_helper, 
    Stuff,
    StuffImage,
    StuffFilmography
)
from core.schemas import (
    StuffRead,
    StuffSearchResponse,
    StuffImageRead,
    StuffFilmographyRead,
)

router = APIRouter(
    prefix="/stuff",
    tags=["Stuff"],
)


# GET /api/v1/stuff/ - Список всех участников индустрии (актеры, режиссеры и др.)
@router.get("/", response_model=StuffSearchResponse, summary="Список участников")
async def list_stuff(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список участников с пагинацией"""
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * page_size
    
    # Получаем общее количество участников
    total_count_stmt = select(func.count(Stuff.id))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем участников для текущей страницы
    stmt = (
        select(Stuff)
        .order_by(Stuff.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    stuff_list = result.scalars().all()
    
    items = [StuffRead.model_validate(person) for person in stuff_list]
    
    return StuffSearchResponse(
        items=items,
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/stuff/kinopoisk/12345 - Найти участника по его оригинальному ID Кинопоиска
@router.get("/kinopoisk/{kinopoisk_id}", response_model=StuffRead, summary="Участник по Кинопоиск ID")
async def get_stuff_by_kinopoisk_id(
    kinopoisk_id: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить участника по его Кинопоиск ID"""
    stmt = select(Stuff).where(Stuff.kinopoisk_id == kinopoisk_id)
    result = await session.execute(stmt)
    person = result.scalar_one_or_none()
    
    if not person:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    return StuffRead.model_validate(person)


# GET /api/v1/stuff/search?query=Брэд Питт - Поиск участника по русскому или английскому имени
@router.get("/search", response_model=StuffSearchResponse, summary="Поиск участников по имени")
async def search_stuff(
    query: str = Query(..., min_length=1, description="Строка поиска"),
    lang: str = Query("ru", description="Язык имени: 'ru' (name_ru) или 'en' (name_en)"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Поиск участников по имени"""
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")
    
    offset = (page - 1) * page_size
    pattern = f"%{query}%"
    
    search_column = Stuff.name_ru if lang == "ru" else Stuff.name_en
    
    total_count_stmt = select(func.count(Stuff.id)).where(search_column.ilike(pattern))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    stmt = (
        select(Stuff)
        .where(search_column.ilike(pattern))
        .order_by(Stuff.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    stuff_list = result.scalars().all()
    
    return StuffSearchResponse(
        items=[StuffRead.model_validate(person) for person in stuff_list],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/stuff/1/images - Фотографии и промо-снимки с участием данной личности
@router.get("/{stuff_id}/images", response_model=List[StuffImageRead], summary="Изображения участника")
async def get_stuff_images(
    stuff_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить изображения участника"""
    stmt = (
        select(StuffImage)
        .where(StuffImage.stuff_id == stuff_id)
        .order_by(StuffImage.image_type, StuffImage.id)
    )
    result = await session.execute(stmt)
    images = result.scalars().all()
    return [StuffImageRead.model_validate(img) for img in images]


# GET /api/v1/stuff/1/filmography - Список всех проектов, в которых принимал участие человек
@router.get("/{stuff_id}/filmography", response_model=List[StuffFilmographyRead], summary="Фильмография участника")
async def get_stuff_filmography(
    stuff_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить фильмографию участника"""
    stmt = (
        select(StuffFilmography)
        .where(StuffFilmography.stuff_id == stuff_id)
        .order_by(StuffFilmography.release_year.desc().nullslast(), StuffFilmography.id)
    )
    result = await session.execute(stmt)
    filmography = result.scalars().all()
    return [StuffFilmographyRead.model_validate(item) for item in filmography]


# GET /api/v1/stuff/1 - Полная биография и детали участника по его внутреннему ID
@router.get("/{stuff_id}", response_model=StuffRead, summary="Детали участника")
async def get_stuff(
    stuff_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали участника по ID"""
    stmt = select(Stuff).where(Stuff.id == stuff_id)
    result = await session.execute(stmt)
    person = result.scalar_one_or_none()
    
    if not person:
        raise HTTPException(status_code=404, detail="Stuff not found")
    
    return StuffRead.model_validate(person)
