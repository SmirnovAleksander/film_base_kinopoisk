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
    SeriesSearchResponse,
    GenreRead,
    CountryRead,
    StuffRead,
    ContentImageRead,
    ContentWatchProviderRead,
    SimilarContentRead,
    SeriesRecommendationRead,
    SeriesRecommendationsResponse,
)

router = APIRouter(
    prefix="/series",
    tags=["Series"],
)


# GET /api/v1/series/ - Получить основной список сериалов с пагинацией
@router.get("/", response_model=SeriesSearchResponse, summary="Список сериалов")
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
        .options(selectinload(Series.user_rating))
        .order_by(Series.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    series_list = result.scalars().all()
    
    return SeriesSearchResponse(
        items=[SeriesRead.model_validate(series) for series in series_list],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/series/search?query=друзья - Поиск сериала по русскому или английскому названию
@router.get("/search", response_model=SeriesSearchResponse, summary="Поиск сериалов по названию")
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
        .options(selectinload(Series.user_rating))
        .where(search_column.ilike(pattern))
        .order_by(Series.rating_kp.desc().nullslast(), Series.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    series_list = result.scalars().all()
    
    return SeriesSearchResponse(
        items=[SeriesRead.model_validate(series) for series in series_list],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/series/filter?genre_id=1&start_year=2020 - Расширенный поиск сериалов по нескольким критериям
@router.get("/filter", response_model=SeriesSearchResponse, summary="Сериалы по фильтрам")
async def series_filter(
    genre_id: Optional[int] = Query(None, description="ID жанра"),
    country_id: Optional[int] = Query(None, description="ID страны"),
    start_year: Optional[int] = Query(None, description="Начальный год"),
    end_year: Optional[int] = Query(None, description="Конечный год"),
    title: Optional[str] = Query(None, min_length=1, description="Поисковая строка по названию"),
    lang: str = Query("ru", description="Язык названия: 'ru' или 'en'"),
    source: str = Query("kp", description="Источник рейтинга: 'kp' или 'imdb'"),
    min_rating: Optional[float] = Query(None, description="Минимальный рейтинг"),
    max_rating: Optional[float] = Query(None, description="Максимальный рейтинг"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Фильтрация сериалов по различным параметрам"""
    if source not in ("kp", "imdb"):
        raise HTTPException(status_code=400, detail="source must be 'kp' or 'imdb'")
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")
    
    offset = (page - 1) * page_size
    
    # Базовый запрос
    stmt = select(Series)
    conditions = []
    
    # Фильтр по жанру
    if genre_id is not None:
        stmt = stmt.join(Series.genres)
        conditions.append(Genre.id == genre_id)
    
    # Фильтр по стране
    if country_id is not None:
        stmt = stmt.join(Series.countries)
        conditions.append(Country.id == country_id)
    
    # Фильтр по году
    if start_year is not None and end_year is None:
        conditions.append(Series.release_year == start_year)
    elif end_year is not None:
        if start_year is not None:
            conditions.append(Series.release_year >= start_year)
        conditions.append(Series.release_year <= end_year)
    
    # Фильтр по названию
    if title is not None and title.strip():
        search_column = Series.title_ru if lang == "ru" else Series.title_en
        conditions.append(search_column.ilike(f"%{title}%"))
    
    # Фильтр по рейтингу
    rating_column = Series.rating_kp if source == "kp" else Series.rating_imdb
    if min_rating is not None:
        conditions.append(rating_column >= min_rating)
    if max_rating is not None:
        conditions.append(rating_column <= max_rating)
    
    # Применяем условия
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    # Подсчет общего количества
    count_stmt = select(func.count(Series.id.distinct()))
    if genre_id is not None:
        count_stmt = count_stmt.join(Series.genres)
    if country_id is not None:
        count_stmt = count_stmt.join(Series.countries)
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))
    
    total_count_result = await session.execute(count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем сериалы
    stmt = (
        stmt
        .options(selectinload(Series.user_rating))
        .order_by(Series.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    series_list = result.scalars().all()
    
    return SeriesSearchResponse(
        items=[SeriesRead.model_validate(series) for series in series_list],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# GET /api/v1/series/kinopoisk/258687 - Найти сериал в базе по его оригинальному ID Кинопоиска
@router.get("/kinopoisk/{kinopoisk_id}", response_model=SeriesReadWithDetails, summary="Сериал по Кинопоиск ID")
async def get_series_by_kinopoisk_id(
    kinopoisk_id: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить сериал по его Кинопоиск ID"""
    stmt = (
        select(Series)
        .options(
            selectinload(Series.genres),
            selectinload(Series.countries),
            selectinload(Series.stuff),
            selectinload(Series.images),
            selectinload(Series.watch_providers),
            selectinload(Series.similar_content),
            selectinload(Series.user_rating),
        )
        .where(Series.kinopoisk_id == kinopoisk_id)
    )
    result = await session.execute(stmt)
    series = result.scalar_one_or_none()
    
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    
    return SeriesReadWithDetails.model_validate(series)


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
            selectinload(Series.user_rating),
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


# GET /api/v1/series/1/recommendations - Рекомендации на основе жанров, участников и рейтинга
@router.get("/{series_id}/recommendations", response_model=SeriesRecommendationsResponse, summary="Рекомендуемые сериалы")
async def get_series_recommendations(
    series_id: int,
    limit: int = Query(10, ge=1, le=50, description="Количество рекомендаций"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Получить рекомендации сериалов на основе контентной фильтрации:
    - Жанры (40%)
    - Участники (30%)
    - Год выпуска (15%)
    - Рейтинг (15%)
    """
    # Проверяем, что сериал существует
    series_stmt = (
        select(Series)
        .options(
            selectinload(Series.genres),
            selectinload(Series.stuff)
        )
        .where(Series.id == series_id)
    )
    series_result = await session.execute(series_stmt)
    current_series = series_result.scalar_one_or_none()
 
    if not current_series:
        raise HTTPException(status_code=404, detail="Series not found")
 
    # Получаем данные текущего сериала
    current_genres = [genre.name for genre in current_series.genres]
    current_stuff_ids = [stuff.id for stuff in current_series.stuff]
    current_year = current_series.release_year
    current_rating = current_series.rating_kp
 
    # Получаем кандидатов для рекомендаций (исключаем текущий сериал)
    candidates_stmt = (
        select(Series)
        .options(
            selectinload(Series.genres),
            selectinload(Series.stuff),
            selectinload(Series.user_rating)
        )
        .where(Series.id != series_id)
        .where(Series.title_ru.isnot(None))
        .order_by(Series.rating_kp.desc().nullslast())
        .limit(200)
    )
    candidates_result = await session.execute(candidates_stmt)
    candidates = candidates_result.scalars().all()
 
    recommendations = []
 
    for candidate in candidates:
        candidate_year = candidate.release_year
        candidate_rating = candidate.rating_kp
 
        # Подсчет совпадений по жанрам (40%)
        candidate_genres = [genre.name for genre in candidate.genres]
        genre_matches = len(set(current_genres) & set(candidate_genres))
        genre_score = (genre_matches / max(len(current_genres), 1)) * 0.4
 
        # Подсчет совпадений по участникам (30%)
        candidate_stuff_ids = [stuff.id for stuff in candidate.stuff]
        stuff_matches = len(set(current_stuff_ids) & set(candidate_stuff_ids))
        stuff_score = (stuff_matches / max(len(current_stuff_ids), 1)) * 0.3
 
        # Близость по году (15%)
        if current_year and candidate_year:
            year_diff = abs(current_year - candidate_year)
            year_score = max(0, (10 - year_diff) / 10) * 0.15
        else:
            year_score = 0
 
        # Близость по рейтингу (15%)
        if current_rating and candidate_rating:
            rating_diff = abs(float(current_rating) - float(candidate_rating))
            rating_score = max(0, (2 - rating_diff) / 2) * 0.15
        else:
            rating_score = 0
 
        # Общий скор
        total_score = genre_score + stuff_score + year_score + rating_score
 
        if total_score > 0.1:  # Минимальный порог релевантности
            # Создаем объект через Pydantic валидацию
            series_data = SeriesRead.model_validate(candidate)
            recommendation = SeriesRecommendationRead(
                **series_data.model_dump(),
                relevance_score=round(total_score, 3),
                genre_matches=genre_matches,
                stuff_matches=stuff_matches
            )
            recommendations.append(recommendation)
 
    # Сортируем по релевантности и возвращаем топ
    recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
 
    return SeriesRecommendationsResponse(
        items=recommendations[:limit],
        total_count=len(recommendations)
    )
