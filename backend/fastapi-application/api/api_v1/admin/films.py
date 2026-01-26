from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.models import db_helper, Film
from core.schemas import (
    FilmRead,
    FilmCreate,
    FilmUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/films",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/films - Создать новую запись о фильме в базе данных
@router.post("", response_model=FilmRead, summary="Создать фильм")
async def create_film(
    film_data: FilmCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новый фильм (только для суперпользователя)"""
    # Проверяем, существует ли фильм с таким kinopoisk_id
    stmt = select(Film).where(Film.kinopoisk_id == film_data.kinopoisk_id)
    result = await session.execute(stmt)
    existing_film = result.scalar_one_or_none()

    if existing_film:
        raise HTTPException(status_code=400, detail="Film with this kinopoisk_id already exists")

    # Создаем новый фильм
    new_film = Film(**film_data.model_dump(exclude_unset=True))
    session.add(new_film)
    await session.commit()
    
    # Перезагружаем со связями для валидации схемы
    stmt = select(Film).options(selectinload(Film.user_rating)).where(Film.id == new_film.id)
    new_film = (await session.execute(stmt)).scalar_one()

    return FilmRead.model_validate(new_film)


# GET /api/v1/admin/films - Список всех фильмов в базе с расширенной пагинацией
@router.get("", response_model=list[FilmRead], summary="Список фильмов")
async def list_films_admin(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(50, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех фильмов с пагинацией (только для суперпользователя)"""
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

    return [FilmRead.model_validate(film) for film in films]


# GET /api/v1/admin/films/1 - Получить технические детали фильма по его ID
@router.get("/{film_id}", response_model=FilmRead, summary="Детали фильма")
async def get_film_admin(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали фильма по ID (только для суперпользователя)"""
    stmt = select(Film).options(selectinload(Film.user_rating)).where(Film.id == film_id)
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    return FilmRead.model_validate(film)


# PUT /api/v1/admin/films/1 - Полностью или частично обновить данные о фильме
@router.put("/{film_id}", response_model=FilmRead, summary="Обновить фильм")
async def update_film_admin(
    film_id: int,
    film_data: FilmUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить фильм (только для суперпользователя)"""
    stmt = select(Film).options(selectinload(Film.user_rating)).where(Film.id == film_id)
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    # Обновляем поля фильма
    update_data = film_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(film, field, value)

    await session.commit()
    
    # Перезагружаем со связями для валидации схемы
    stmt = select(Film).options(selectinload(Film.user_rating)).where(Film.id == film_id)
    film = (await session.execute(stmt)).scalar_one()

    return FilmRead.model_validate(film)


# DELETE /api/v1/admin/films/1 - Навсегда удалить запись о фильме из базы данных
@router.delete("/{film_id}", response_model=OperationResponse, summary="Удалить фильм")
async def delete_film_admin(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить фильм (только для суперпользователя)"""
    stmt = select(Film).where(Film.id == film_id)
    result = await session.execute(stmt)
    film = result.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    await session.delete(film)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Film deleted successfully",
        id=film_id
    )
