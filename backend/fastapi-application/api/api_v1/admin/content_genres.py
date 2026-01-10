from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.models import db_helper, Genre
from core.models.associations import content_genre
from core.schemas import (
    ContentGenreRead,
    ContentGenreCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/content-genres",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/content-genres - Связать фильм или сериал с конкретным жанром
@router.post("", response_model=ContentGenreRead, summary="Создать связь контент-жанр")
async def create_content_genre_admin(
    cgi_data: ContentGenreCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь между контентом и жанром (только для суперпользователя)"""
    # Проверяем, что жанр существует
    genre_stmt = select(Genre).where(Genre.id == cgi_data.genre_id)
    genre_result = await session.execute(genre_stmt)
    genre = genre_result.scalar_one_or_none()
    
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # Проверяем, не существует ли уже такая связь
    check_stmt = select(content_genre).where(
        content_genre.c.content_id == cgi_data.content_id,
        content_genre.c.content_type == cgi_data.content_type,
        content_genre.c.genre_id == cgi_data.genre_id
    )
    check_result = await session.execute(check_stmt)
    existing = check_result.first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Content-Genre association already exists")
    
    # Создаем связь
    insert_stmt = insert(content_genre).values(
        content_id=cgi_data.content_id,
        content_type=cgi_data.content_type,
        genre_id=cgi_data.genre_id
    ).returning(content_genre.c.id, content_genre.c.content_id, content_genre.c.content_type, content_genre.c.genre_id)
    
    result = await session.execute(insert_stmt)
    await session.commit()
    
    row = result.first()
    return ContentGenreRead(
        id=row.id,
        content_id=row.content_id,
        content_type=row.content_type,
        genre_id=row.genre_id
    )


# GET /api/v1/admin/content-genres?content_id=1 - Получить список всех жанровых привязок
@router.get("", response_model=list[ContentGenreRead], summary="Список связей контент-жанр")
async def list_content_genres_admin(
    content_id: Optional[int] = Query(None, description="Фильтр по ID контента"),
    content_type: Optional[str] = Query(None, description="Фильтр по типу контента"),
    genre_id: Optional[int] = Query(None, description="Фильтр по ID жанра"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список связей контент-жанр (только для суперпользователя)"""
    stmt = select(content_genre)
    
    conditions = []
    if content_id:
        conditions.append(content_genre.c.content_id == content_id)
    if content_type:
        conditions.append(content_genre.c.content_type == content_type)
    if genre_id:
        conditions.append(content_genre.c.genre_id == genre_id)
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    result = await session.execute(stmt)
    rows = result.all()
    
    return [
        ContentGenreRead(
            id=row.id,
            content_id=row.content_id,
            content_type=row.content_type,
            genre_id=row.genre_id
        )
        for row in rows
    ]


# GET /api/v1/admin/content-genres/1 - Информация о конкретной записи привязки жанра
@router.get("/{association_id}", response_model=ContentGenreRead, summary="Детали связи контент-жанр")
async def get_content_genre_admin(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи по ID (только для суперпользователя)"""
    stmt = select(content_genre).where(content_genre.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Content-Genre association not found")
    
    return ContentGenreRead(
        id=row.id,
        content_id=row.content_id,
        content_type=row.content_type,
        genre_id=row.genre_id
    )


# DELETE /api/v1/admin/content-genres/1 - Удалить связь фильма/сериала с жанром
@router.delete("/{association_id}", response_model=OperationResponse, summary="Удалить связь контент-жанр")
async def delete_content_genre_admin(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь контент-жанр (только для суперпользователя)"""
    stmt = select(content_genre).where(content_genre.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Content-Genre association not found")
    
    delete_stmt = delete(content_genre).where(content_genre.c.id == association_id)
    await session.execute(delete_stmt)
    await session.commit()
    
    return OperationResponse(
        status="success",
        message="Content-Genre association deleted successfully",
        id=association_id
    )
