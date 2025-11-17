from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.models import db_helper, Film, Country
from core.models.associations import film_country
from core.schemas import (
    FilmCountryRead,
    FilmCountryCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/film-countries",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=FilmCountryRead, summary="Создать связь фильм-страна")
async def create_film_country(
    film_country_data: FilmCountryCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь между фильмом и страной (только для суперпользователя)"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_country_data.film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Проверяем, что страна существует
    country_stmt = select(Country).where(Country.id == film_country_data.country_id)
    country_result = await session.execute(country_stmt)
    country = country_result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    # Проверяем, не существует ли уже такая связь
    check_stmt = select(film_country).where(
        film_country.c.film_id == film_country_data.film_id,
        film_country.c.country_id == film_country_data.country_id
    )
    check_result = await session.execute(check_stmt)
    existing = check_result.first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Film-Country association already exists")
    
    # Создаем связь
    insert_stmt = insert(film_country).values(
        film_id=film_country_data.film_id,
        country_id=film_country_data.country_id
    ).returning(film_country.c.id, film_country.c.film_id, film_country.c.country_id)
    
    result = await session.execute(insert_stmt)
    await session.commit()
    
    row = result.first()
    return FilmCountryRead(
        id=row.id,
        film_id=row.film_id,
        country_id=row.country_id
    )


@router.get("", response_model=list[FilmCountryRead], summary="Список связей фильм-страна")
async def list_film_countries(
    film_id: Optional[int] = Query(None, description="Фильтр по ID фильма"),
    country_id: Optional[int] = Query(None, description="Фильтр по ID страны"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список связей фильм-страна (только для суперпользователя)"""
    stmt = select(film_country)
    
    if film_id:
        stmt = stmt.where(film_country.c.film_id == film_id)
    if country_id:
        stmt = stmt.where(film_country.c.country_id == country_id)
    
    result = await session.execute(stmt)
    rows = result.all()
    
    return [
        FilmCountryRead(
            id=row.id,
            film_id=row.film_id,
            country_id=row.country_id
        )
        for row in rows
    ]


@router.get("/{association_id}", response_model=FilmCountryRead, summary="Детали связи фильм-страна")
async def get_film_country(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи по ID (только для суперпользователя)"""
    stmt = select(film_country).where(film_country.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Country association not found")
    
    return FilmCountryRead(
        id=row.id,
        film_id=row.film_id,
        country_id=row.country_id
    )


@router.delete("/{association_id}", response_model=OperationResponse, summary="Удалить связь фильм-страна")
async def delete_film_country(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь фильм-страна (только для суперпользователя)"""
    # Проверяем существование связи
    stmt = select(film_country).where(film_country.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Country association not found")
    
    # Удаляем связь
    delete_stmt = delete(film_country).where(film_country.c.id == association_id)
    await session.execute(delete_stmt)
    await session.commit()
    
    return OperationResponse(
        status="success",
        message="Film-Country association deleted successfully",
        id=association_id
    )

