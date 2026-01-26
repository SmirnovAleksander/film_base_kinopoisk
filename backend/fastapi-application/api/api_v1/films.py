from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from core.models import ( 
    db_helper, 
    Film, 
    Genre, 
    Country, 
    Stuff, 
    ContentImage, 
    ContentWatchProvider, 
    SimilarContent 
    )
from core.models.associations import content_stuff
from core.schemas import (
    FilmRead,
    FilmReadWithDetails,
    FilmSearchResponse,
    FilmRecommendationRead,
    FilmRecommendationsResponse,
    GenreRead,
    CountryRead,
    StuffRead,
    ContentImageRead,
    ContentWatchProviderRead,
    SimilarContentRead,
)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
)


# GET /api/v1/films/ - Получить основной список фильмов с пагинацией
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
        .options(selectinload(Film.user_rating))
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


# GET /api/v1/films/search?query=интерстеллар - Поиск фильма по русскому или английскому названию
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
    search_column = Film.title_ru if lang == "ru" else Film.title_en
    
    # Подсчет общего количества
    total_count_stmt = select(func.count(Film.id)).where(search_column.ilike(pattern))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем фильмы
    stmt = (
        select(Film)
        .options(selectinload(Film.user_rating))
        .where(search_column.ilike(pattern))
        .order_by(Film.rating_kp.desc().nullslast(), Film.id)
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


# GET /api/v1/films/filter?genre_id=1&start_year=2020 - Расширенный поиск фильмов по нескольким критериям
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
        conditions.append(Film.release_year == start_year)
    elif end_year is not None:
        if start_year is not None:
            conditions.append(Film.release_year >= start_year)
        conditions.append(Film.release_year <= end_year)
    
    # Фильтр по названию
    if title is not None and title.strip():
        search_column = Film.title_ru if lang == "ru" else Film.title_en
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
    stmt = (
        stmt
        .options(selectinload(Film.user_rating))
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


# GET /api/v1/films/kinopoisk/258687 - Найти фильм в базе по его оригинальному ID Кинопоиска
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
            selectinload(Film.stuff),
            selectinload(Film.images),
            selectinload(Film.watch_providers),
            selectinload(Film.similar_content),
            selectinload(Film.user_rating),
        )
        .where(Film.kinopoisk_id == kinopoisk_id)
    )
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    return FilmReadWithDetails.model_validate(film)


# GET /api/v1/films/1 - Получить полную информацию о фильме по его внутреннему ID
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
            selectinload(Film.stuff),
            selectinload(Film.images),
            selectinload(Film.watch_providers),
            selectinload(Film.similar_content),
            selectinload(Film.user_rating),
        )
        .where(Film.id == film_id)
    )
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    return FilmReadWithDetails.model_validate(film)


# GET /api/v1/films/1/watch-providers - Список платформ (Okko, Иви и др.), где доступен фильм
@router.get("/{film_id}/watch-providers", response_model=List[ContentWatchProviderRead], summary="Провайдеры для просмотра")
async def get_watch_providers(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить провайдеров для просмотра фильма"""
    stmt = (
        select(ContentWatchProvider)
        .where(
            and_(
                ContentWatchProvider.content_id == film_id,
                ContentWatchProvider.content_type == "film"
            )
        )
        .order_by(ContentWatchProvider.provider_name)
    )
    result = await session.execute(stmt)
    providers = result.scalars().all()
    
    return [ContentWatchProviderRead.model_validate(provider) for provider in providers]


# GET /api/v1/films/1/similar - Получить список похожих фильмов из базы
@router.get("/{film_id}/similar", response_model=List[SimilarContentRead], summary="Похожие фильмы")
async def get_similar_films(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить похожие фильмы"""
    stmt = (
        select(SimilarContent)
        .where(
            and_(
                SimilarContent.content_id == film_id,
                SimilarContent.content_type == "film"
            )
        )
        .order_by(SimilarContent.id)
    )
    result = await session.execute(stmt)
    similar_films = result.scalars().all()
    
    return [SimilarContentRead.model_validate(similar_film) for similar_film in similar_films]


# GET /api/v1/films/1/stills - Ссылки на кадры, обои и скриншоты из фильма
@router.get("/{film_id}/stills", summary="Кадры и обои фильма")
async def get_film_stills(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить кадры и обои фильма"""
    # Разрешенные типы
    ALLOWED_TYPES = {"stills", "wall", "shooting", "screenshots"}
    
    stmt = (
        select(ContentImage)
        .where(
            and_(
                ContentImage.content_id == film_id,
                ContentImage.content_type == "film"
            )
        )
        .order_by(ContentImage.image_type, ContentImage.picture_id)
    )
    result = await session.execute(stmt)
    stills = result.scalars().all()
    
    # Группируем по источнику, включая только разрешенные типы
    grouped = {type_name: [] for type_name in ALLOWED_TYPES}
    for still in stills:
        still_data = {
            "id": still.picture_id,
            "original": still.image_url
        }
        if still.image_type in ALLOWED_TYPES:
            grouped[still.image_type].append(still_data)
    
    # Убираем пустые массивы для более чистого ответа
    return {k: v for k, v in grouped.items() if v}


# GET /api/v1/films/1/stuff?role=actor - Список участников (актеры, режиссеры) конкретного фильма
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
        Stuff.__table__.join(content_stuff).join(Film.__table__, Film.id == content_stuff.c.content_id)
    ).where(
        and_(
            content_stuff.c.content_id == film_id,
            content_stuff.c.content_type == "film"
        )
    )

    if role and role.lower() != "all":
        stmt = stmt.where(content_stuff.c.role == role)

    stmt = stmt.order_by(Stuff.id)
    result = await session.execute(stmt)
    stuff = result.scalars().all()

    return [StuffRead.model_validate(person) for person in stuff]


# GET /api/v1/films/1/recommendations - Рекомендации на основе жанров, участников и рейтинга
@router.get("/{film_id}/recommendations", response_model=FilmRecommendationsResponse, summary="Рекомендуемые фильмы")
async def get_film_recommendations(
    film_id: int,
    limit: int = Query(10, ge=1, le=50, description="Количество рекомендаций"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Получить рекомендации фильмов на основе контентной фильтрации:
    - Жанры (40%)
    - Участники (30%)
    - Год выпуска (15%)
    - Рейтинг (15%)
    """
    # Проверяем, что фильм существует
    film_stmt = (
        select(Film)
        .options(
            selectinload(Film.genres),
            selectinload(Film.stuff)
        )
        .where(Film.id == film_id)
    )
    film_result = await session.execute(film_stmt)
    current_film = film_result.scalar_one_or_none()

    if not current_film:
        raise HTTPException(status_code=404, detail="Film not found")

    # Получаем данные текущего фильма
    current_genres = [genre.name for genre in current_film.genres]
    current_stuff_ids = [stuff.id for stuff in current_film.stuff]
    current_year = current_film.release_year
    current_rating = current_film.rating_kp

    # Получаем кандидатов для рекомендаций (исключаем текущий фильм)
    candidates_stmt = (
        select(Film)
        .options(
            selectinload(Film.genres),
            selectinload(Film.stuff),
            selectinload(Film.user_rating)
        )
        .where(Film.id != film_id)
        .where(Film.title_ru.isnot(None))
        .order_by(Film.rating_kp.desc().nullslast())
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
            film_data = FilmRead.model_validate(candidate)
            recommendation = FilmRecommendationRead(
                **film_data.model_dump(),
                relevance_score=round(total_score, 3),
                genre_matches=genre_matches,
                stuff_matches=stuff_matches
            )
            recommendations.append(recommendation)

    # Сортируем по релевантности и возвращаем топ
    recommendations.sort(key=lambda x: x.relevance_score, reverse=True)

    return FilmRecommendationsResponse(
        items=recommendations[:limit],
        total_count=len(recommendations)
    )
