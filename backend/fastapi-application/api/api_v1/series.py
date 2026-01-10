from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from core.models import ( 
    db_helper, 
    Series, 
    Genre, 
    Country, 
    Stuff, 
    ContentImage, 
    ContentWatchProvider, 
    SimilarContent 
    )
from core.models.associations import content_stuff
from core.schemas import (
    SeriesRead,
    SeriesReadWithDetails,
    FilmSearchResponse, # Can reuse this or rename it
    GenreRead,
    CountryRead,
    StuffRead,
    ContentImageRead,
    ContentWatchProviderRead,
    SimilarContentRead,
)

router = APIRouter(
    prefix="/series",
    tags=["Series"],
)


# GET /api/v1/series/ - Получить основной список сериалов с пагинацией
@router.get("/", response_model=FilmSearchResponse, summary="Список сериалов")
async def list_series(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список сериалов с пагинацией"""
    offset = (page - 1) * page_size
    
    # Получаем общее количество
    total_count_stmt = select(func.count(Series.id))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем сериалы
    stmt = (
        select(Series)
        .order_by(Series.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    series_list = result.scalars().all()
    
    return FilmSearchResponse(
        items=[SeriesRead.model_validate(series) for series in series_list],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/series/search?query=друзья - Поиск сериала по русскому или английскому названию
@router.get("/search", response_model=FilmSearchResponse, summary="Поиск сериалов по названию")
async def search_series(
    query: str = Query(..., min_length=1, description="Строка поиска"),
    lang: str = Query("ru", description="Язык названия: 'ru' (title_ru) или 'en' (title_en)"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Поиск сериалов по названию"""
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")
    
    offset = (page - 1) * page_size
    pattern = f"%{query}%"
    
    search_column = Series.title_ru if lang == "ru" else Series.title_en
    
    total_count_stmt = select(func.count(Series.id)).where(search_column.ilike(pattern))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    stmt = (
        select(Series)
        .where(search_column.ilike(pattern))
        .order_by(Series.rating_kp.desc().nullslast(), Series.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    series_list = result.scalars().all()
    
    return FilmSearchResponse(
        items=[SeriesRead.model_validate(series) for series in series_list],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/series/1 - Получить подробную информацию о сериале по его внутреннему ID
@router.get("/{series_id}", response_model=SeriesReadWithDetails, summary="Детали сериала")
async def get_series(
    series_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали сериала по ID"""
    stmt = (
        select(Series)
        .options(
            selectinload(Series.genres),
            selectinload(Series.countries),
            selectinload(Series.stuff),
            selectinload(Series.images),
            selectinload(Series.watch_providers),
            selectinload(Series.similar_content),
        )
        .where(Series.id == series_id)
    )
    result = await session.execute(stmt)
    series = result.scalar_one_or_none()
    
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    
    return SeriesReadWithDetails.model_validate(series)


# GET /api/v1/series/1/watch-providers - Список платформ (Okko, Иви и др.), где можно посмотреть сериал
@router.get("/{series_id}/watch-providers", response_model=List[ContentWatchProviderRead], summary="Провайдеры для просмотра")
async def get_watch_providers(
    series_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить провайдеров для просмотра сериала"""
    stmt = (
        select(ContentWatchProvider)
        .where(
            and_(
                ContentWatchProvider.content_id == series_id,
                ContentWatchProvider.content_type == "series"
            )
        )
        .order_by(ContentWatchProvider.provider_name)
    )
    result = await session.execute(stmt)
    providers = result.scalars().all()
    
    return [ContentWatchProviderRead.model_validate(provider) for provider in providers]


# GET /api/v1/series/1/similar - Список похожих сериалов из базы
@router.get("/{series_id}/similar", response_model=List[SimilarContentRead], summary="Похожие сериалы")
async def get_similar_series(
    series_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить похожие сериалы"""
    stmt = (
        select(SimilarContent)
        .where(
            and_(
                SimilarContent.content_id == series_id,
                SimilarContent.content_type == "series"
            )
        )
        .order_by(SimilarContent.id)
    )
    result = await session.execute(stmt)
    similar_content = result.scalars().all()
    
    return [SimilarContentRead.model_validate(similar) for similar in similar_content]


# GET /api/v1/series/1/stills - Ссылки на промо-материалы, кадры и скриншоты сериала
@router.get("/{series_id}/stills", summary="Кадры и обои сериала")
async def get_series_stills(
    series_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить кадры и обои сериала"""
    ALLOWED_TYPES = {"stills", "wall", "shooting", "screenshots"}
    
    stmt = (
        select(ContentImage)
        .where(
            and_(
                ContentImage.content_id == series_id,
                ContentImage.content_type == "series"
            )
        )
        .order_by(ContentImage.image_type, ContentImage.picture_id)
    )
    result = await session.execute(stmt)
    stills = result.scalars().all()
    
    grouped = {type_name: [] for type_name in ALLOWED_TYPES}
    for still in stills:
        still_data = {
            "id": still.picture_id,
            "original": still.image_url
        }
        if still.image_type in ALLOWED_TYPES:
            grouped[still.image_type].append(still_data)
    
    return {k: v for k, v in grouped.items() if v}


# GET /api/v1/series/1/stuff?role=actor - Список участников (актеры, режиссеры) конкретного сериала
@router.get("/{series_id}/stuff", response_model=List[StuffRead], summary="Участники сериала")
async def get_series_stuff(
    series_id: int,
    role: str = Query("all", description="Роль участника или 'all' для всех"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить участников сериала"""
    series_stmt = select(Series).where(Series.id == series_id)
    series_result = await session.execute(series_stmt)
    series = series_result.scalar_one_or_none()

    if not series:
        raise HTTPException(status_code=404, detail="Series not found")

    stmt = select(Stuff).select_from(
        Stuff.__table__.join(content_stuff).join(Series.__table__, Series.id == content_stuff.c.content_id)
    ).where(
        and_(
            content_stuff.c.content_id == series_id,
            content_stuff.c.content_type == "series"
        )
    )

    if role and role.lower() != "all":
        stmt = stmt.where(content_stuff.c.role == role)

    stmt = stmt.order_by(Stuff.id)
    result = await session.execute(stmt)
    stuff = result.scalars().all()

    return [StuffRead.model_validate(person) for person in stuff]
