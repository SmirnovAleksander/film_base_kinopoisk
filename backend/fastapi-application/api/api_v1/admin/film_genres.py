from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.models import db_helper, Film, Genre
from core.models.associations import film_genre
from core.schemas import (
    FilmGenreRead,
    FilmGenreCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/film-genres",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=FilmGenreRead, summary="Создать связь фильм-жанр")
async def create_film_genre(
    film_genre_data: FilmGenreCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь между фильмом и жанром (только для суперпользователя)"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_genre_data.film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Проверяем, что жанр существует
    genre_stmt = select(Genre).where(Genre.id == film_genre_data.genre_id)
    genre_result = await session.execute(genre_stmt)
    genre = genre_result.scalar_one_or_none()
    
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # Проверяем, не существует ли уже такая связь
    check_stmt = select(film_genre).where(
        film_genre.c.film_id == film_genre_data.film_id,
        film_genre.c.genre_id == film_genre_data.genre_id
    )
    check_result = await session.execute(check_stmt)
    existing = check_result.first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Film-Genre association already exists")
    
    # Создаем связь
    insert_stmt = insert(film_genre).values(
        film_id=film_genre_data.film_id,
        genre_id=film_genre_data.genre_id
    ).returning(film_genre.c.id, film_genre.c.film_id, film_genre.c.genre_id)
    
    result = await session.execute(insert_stmt)
    await session.commit()
    
    row = result.first()
    return FilmGenreRead(
        id=row.id,
        film_id=row.film_id,
        genre_id=row.genre_id
    )


@router.get("", response_model=list[FilmGenreRead], summary="Список связей фильм-жанр")
async def list_film_genres(
    film_id: Optional[int] = Query(None, description="Фильтр по ID фильма"),
    genre_id: Optional[int] = Query(None, description="Фильтр по ID жанра"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список связей фильм-жанр (только для суперпользователя)"""
    stmt = select(film_genre)
    
    if film_id:
        stmt = stmt.where(film_genre.c.film_id == film_id)
    if genre_id:
        stmt = stmt.where(film_genre.c.genre_id == genre_id)
    
    result = await session.execute(stmt)
    rows = result.all()
    
    return [
        FilmGenreRead(
            id=row.id,
            film_id=row.film_id,
            genre_id=row.genre_id
        )
        for row in rows
    ]


@router.get("/{association_id}", response_model=FilmGenreRead, summary="Детали связи фильм-жанр")
async def get_film_genre(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи по ID (только для суперпользователя)"""
    stmt = select(film_genre).where(film_genre.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Genre association not found")
    
    return FilmGenreRead(
        id=row.id,
        film_id=row.film_id,
        genre_id=row.genre_id
    )


@router.delete("/{association_id}", response_model=OperationResponse, summary="Удалить связь фильм-жанр")
async def delete_film_genre(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь фильм-жанр (только для суперпользователя)"""
    # Проверяем существование связи
    stmt = select(film_genre).where(film_genre.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Genre association not found")
    
    # Удаляем связь
    delete_stmt = delete(film_genre).where(film_genre.c.id == association_id)
    await session.execute(delete_stmt)
    await session.commit()
    
    return OperationResponse(
        status="success",
        message="Film-Genre association deleted successfully",
        id=association_id
    )

