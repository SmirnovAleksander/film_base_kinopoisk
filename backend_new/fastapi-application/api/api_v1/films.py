from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import db_helper, Film, Genre, Country, Stuff, FilmStill, FilmWatchProvider, SimilarFilm
from core.models.associations import film_stuff
from core.schemas import (
    FilmRead,
    FilmReadWithDetails,
    FilmSearchResponse,
    FilmRecommendationRead,
    GenreRead,
    CountryRead,
    StuffRead,
    FilmStillRead,
    FilmWatchProviderRead,
    SimilarFilmRead,
)

router = APIRouter(
    prefix=settings.api.v1.prefix + "/films",
    tags=["Films"],
)


@router.get("/", response_model=FilmSearchResponse, summary="Список фильмов")
async def list_films(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список фильмов с пагинацией"""
    offset = (page - 1) * page_size
    
    # Получаем общее количество фильмов
    total_count_stmt = select(func.count(Film.id))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем фильмы для текущей страницы
    stmt = (
        select(Film)
        .order_by(Film.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    films = result.scalars().all()
    
    return FilmSearchResponse(
        items=[FilmRead.model_validate(film) for film in films],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


@router.get("/search", response_model=FilmSearchResponse, summary="Поиск фильмов по названию")
async def search_films(
    query: str = Query(..., min_length=1, description="Строка поиска"),
    lang: str = Query("ru", description="Язык названия: 'ru' (title) или 'en' (original_title)"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Поиск фильмов по названию"""
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")
    
    offset = (page - 1) * page_size
    pattern = f"%{query}%"
    
    # Выбираем колонку для поиска
    search_column = Film.title if lang == "ru" else Film.original_title
    
    # Подсчет общего количества
    total_count_stmt = select(func.count(Film.id)).where(search_column.ilike(pattern))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем фильмы
    stmt = (
        select(Film)
        .where(search_column.ilike(pattern))
        .order_by(Film.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    films = result.scalars().all()
    
    return FilmSearchResponse(
        items=[FilmRead.model_validate(film) for film in films],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


@router.get("/genres", response_model=List[GenreRead], summary="Все жанры")
async def list_genres(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить список всех жанров"""
    stmt = select(Genre).order_by(Genre.name)
    result = await session.execute(stmt)
    genres = result.scalars().all()
    
    return [GenreRead.model_validate(genre) for genre in genres]


@router.get("/countries", response_model=List[CountryRead], summary="Все страны")
async def list_countries(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить список всех стран"""
    stmt = select(Country).order_by(Country.name)
    result = await session.execute(stmt)
    countries = result.scalars().all()
    
    return [CountryRead.model_validate(country) for country in countries]


@router.get("/filter", response_model=FilmSearchResponse, summary="Фильмы по фильтрам")
async def films_filter(
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
    """Фильтрация фильмов по различным параметрам"""
    if source not in ("kp", "imdb"):
        raise HTTPException(status_code=400, detail="source must be 'kp' or 'imdb'")
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")
    
    offset = (page - 1) * page_size
    
    # Базовый запрос
    stmt = select(Film)
    conditions = []
    
    # Фильтр по жанру
    if genre_id is not None:
        stmt = stmt.join(Film.genres)
        conditions.append(Genre.id == genre_id)
    
    # Фильтр по стране
    if country_id is not None:
        stmt = stmt.join(Film.countries)
        conditions.append(Country.id == country_id)
    
    # Фильтр по году
    if start_year is not None and end_year is None:
        conditions.append(Film.year == start_year)
    elif end_year is not None:
        if start_year is not None:
            conditions.append(Film.year >= start_year)
        conditions.append(Film.year <= end_year)
    
    # Фильтр по названию
    if title is not None and title.strip():
        search_column = Film.title if lang == "ru" else Film.original_title
        conditions.append(search_column.ilike(f"%{title}%"))
    
    # Фильтр по рейтингу
    rating_column = Film.rating_kp if source == "kp" else Film.rating_imdb
    if min_rating is not None:
        conditions.append(rating_column >= min_rating)
    if max_rating is not None:
        conditions.append(rating_column <= max_rating)
    
    # Применяем условия
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    # Подсчет общего количества
    count_stmt = select(func.count(Film.id.distinct()))
    if genre_id is not None:
        count_stmt = count_stmt.join(Film.genres)
    if country_id is not None:
        count_stmt = count_stmt.join(Film.countries)
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))
    
    total_count_result = await session.execute(count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем фильмы
    stmt = stmt.order_by(Film.id).offset(offset).limit(page_size)
    result = await session.execute(stmt)
    films = result.scalars().all()
    
    return FilmSearchResponse(
        items=[FilmRead.model_validate(film) for film in films],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


@router.get("/{film_id}", response_model=FilmReadWithDetails, summary="Детали фильма")
async def get_film(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали фильма по ID"""
    stmt = (
        select(Film)
        .options(
            selectinload(Film.genres),
            selectinload(Film.countries),
        )
        .where(Film.id == film_id)
    )
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    return FilmReadWithDetails.model_validate(film)


@router.get("/kinopoisk/{kinopoisk_id}", response_model=FilmReadWithDetails, summary="Фильм по Кинопоиск ID")
async def get_film_by_kinopoisk_id(
    kinopoisk_id: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить фильм по его Кинопоиск ID"""
    stmt = (
        select(Film)
        .options(
            selectinload(Film.genres),
            selectinload(Film.countries),
        )
        .where(Film.kinopoisk_id == kinopoisk_id)
    )
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    return FilmReadWithDetails.model_validate(film)


@router.get("/{film_id}/watch-providers", response_model=List[FilmWatchProviderRead], summary="Провайдеры для просмотра")
async def get_watch_providers(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить провайдеров для просмотра фильма"""
    stmt = (
        select(FilmWatchProvider)
        .where(FilmWatchProvider.film_id == film_id)
        .order_by(FilmWatchProvider.name)
    )
    result = await session.execute(stmt)
    providers = result.scalars().all()
    
    return [FilmWatchProviderRead.model_validate(provider) for provider in providers]


@router.get("/{film_id}/similar", response_model=List[SimilarFilmRead], summary="Похожие фильмы")
async def get_similar_films(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить похожие фильмы"""
    stmt = (
        select(SimilarFilm)
        .where(SimilarFilm.film_id == film_id)
        .order_by(SimilarFilm.id)
    )
    result = await session.execute(stmt)
    similar_films = result.scalars().all()
    
    return [SimilarFilmRead.model_validate(similar_film) for similar_film in similar_films]


@router.get("/{film_id}/stills", summary="Кадры и обои фильма")
async def get_film_stills(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить кадры и обои фильма"""
    stmt = (
        select(FilmStill)
        .where(FilmStill.film_id == film_id)
        .order_by(FilmStill.source, FilmStill.picture_id)
    )
    result = await session.execute(stmt)
    stills = result.scalars().all()
    
    # Группируем по источнику
    grouped = {"stills": [], "wall": []}
    for still in stills:
        still_data = {
            "id": still.picture_id,
            "original": still.original_url
        }
        if still.source in grouped:
            grouped[still.source].append(still_data)
    
    return grouped


@router.get("/{film_id}/stuff", response_model=List[StuffRead], summary="Участники фильма")
async def get_film_stuff(
    film_id: int,
    role: str = Query("all", description="Роль участника или 'all' для всех"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить участников фильма"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    # Строим запрос с использованием association table
    stmt = select(Stuff).select_from(
        Stuff.__table__.join(film_stuff).join(Film.__table__)
    ).where(film_stuff.c.film_id == film_id)

    if role and role.lower() != "all":
        stmt = stmt.where(film_stuff.c.role == role)

    stmt = stmt.order_by(Stuff.id)
    result = await session.execute(stmt)
    stuff = result.scalars().all()

    return [StuffRead.model_validate(person) for person in stuff]
