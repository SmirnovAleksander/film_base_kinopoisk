from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.models import db_helper, Film, Stuff
from core.models.associations import film_stuff
from core.schemas import (
    FilmStuffRead,
    FilmStuffCreate,
    FilmStuffUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/film-stuff",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=FilmStuffRead, summary="Создать связь фильм-участник")
async def create_film_stuff(
    film_stuff_data: FilmStuffCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь между фильмом и участником (только для суперпользователя)"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_stuff_data.film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Проверяем, что участник существует
    stuff_stmt = select(Stuff).where(Stuff.id == film_stuff_data.stuff_id)
    stuff_result = await session.execute(stuff_stmt)
    stuff = stuff_result.scalar_one_or_none()
    
    if not stuff:
        raise HTTPException(status_code=404, detail="Stuff not found")
    
    # Проверяем, не существует ли уже такая связь с той же ролью
    check_stmt = select(film_stuff).where(
        film_stuff.c.film_id == film_stuff_data.film_id,
        film_stuff.c.stuff_id == film_stuff_data.stuff_id,
        film_stuff.c.role == film_stuff_data.role
    )
    check_result = await session.execute(check_stmt)
    existing = check_result.first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Film-Stuff association with this role already exists")
    
    # Создаем связь
    insert_stmt = insert(film_stuff).values(
        film_id=film_stuff_data.film_id,
        stuff_id=film_stuff_data.stuff_id,
        role=film_stuff_data.role
    ).returning(film_stuff.c.id, film_stuff.c.film_id, film_stuff.c.stuff_id, film_stuff.c.role)
    
    result = await session.execute(insert_stmt)
    await session.commit()
    
    row = result.first()
    return FilmStuffRead(
        id=row.id,
        film_id=row.film_id,
        stuff_id=row.stuff_id,
        role=row.role
    )


@router.get("", response_model=list[FilmStuffRead], summary="Список связей фильм-участник")
async def list_film_stuff(
    film_id: Optional[int] = Query(None, description="Фильтр по ID фильма"),
    stuff_id: Optional[int] = Query(None, description="Фильтр по ID участника"),
    role: Optional[str] = Query(None, description="Фильтр по роли"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список связей фильм-участник (только для суперпользователя)"""
    stmt = select(film_stuff)
    
    if film_id:
        stmt = stmt.where(film_stuff.c.film_id == film_id)
    if stuff_id:
        stmt = stmt.where(film_stuff.c.stuff_id == stuff_id)
    if role:
        stmt = stmt.where(film_stuff.c.role == role)
    
    result = await session.execute(stmt)
    rows = result.all()
    
    return [
        FilmStuffRead(
            id=row.id,
            film_id=row.film_id,
            stuff_id=row.stuff_id,
            role=row.role
        )
        for row in rows
    ]


@router.get("/{association_id}", response_model=FilmStuffRead, summary="Детали связи фильм-участник")
async def get_film_stuff(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи по ID (только для суперпользователя)"""
    stmt = select(film_stuff).where(film_stuff.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Stuff association not found")
    
    return FilmStuffRead(
        id=row.id,
        film_id=row.film_id,
        stuff_id=row.stuff_id,
        role=row.role
    )


@router.put("/{association_id}", response_model=FilmStuffRead, summary="Обновить связь фильм-участник")
async def update_film_stuff(
    association_id: int,
    film_stuff_data: FilmStuffUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить связь фильм-участник (только для суперпользователя)"""
    # Проверяем существование связи
    stmt = select(film_stuff).where(film_stuff.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Stuff association not found")
    
    # Если обновляется роль, проверяем уникальность
    if film_stuff_data.role is not None:
        check_stmt = select(film_stuff).where(
            film_stuff.c.film_id == row.film_id,
            film_stuff.c.stuff_id == row.stuff_id,
            film_stuff.c.role == film_stuff_data.role,
            film_stuff.c.id != association_id
        )
        check_result = await session.execute(check_stmt)
        existing = check_result.first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Film-Stuff association with this role already exists")
    
    # Обновляем связь
    update_data = film_stuff_data.model_dump(exclude_unset=True)
    if update_data:
        update_stmt = update(film_stuff).where(
            film_stuff.c.id == association_id
        ).values(**update_data).returning(
            film_stuff.c.id, film_stuff.c.film_id, film_stuff.c.stuff_id, film_stuff.c.role
        )
        
        result = await session.execute(update_stmt)
        await session.commit()
        
        row = result.first()
        return FilmStuffRead(
            id=row.id,
            film_id=row.film_id,
            stuff_id=row.stuff_id,
            role=row.role
        )
    
    return FilmStuffRead(
        id=row.id,
        film_id=row.film_id,
        stuff_id=row.stuff_id,
        role=row.role
    )


@router.delete("/{association_id}", response_model=OperationResponse, summary="Удалить связь фильм-участник")
async def delete_film_stuff(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь фильм-участник (только для суперпользователя)"""
    # Проверяем существование связи
    stmt = select(film_stuff).where(film_stuff.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Film-Stuff association not found")
    
    # Удаляем связь
    delete_stmt = delete(film_stuff).where(film_stuff.c.id == association_id)
    await session.execute(delete_stmt)
    await session.commit()
    
    return OperationResponse(
        status="success",
        message="Film-Stuff association deleted successfully",
        id=association_id
    )

