from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import db_helper, Genre
from core.schemas import (
    GenreRead,
    GenreCreate,
    GenreUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/genres",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=GenreRead, summary="Создать жанр")
async def create_genre(
    genre_data: GenreCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новый жанр (только для суперпользователя)"""
    # Проверяем, существует ли жанр с таким названием
    stmt = select(Genre).where(Genre.name == genre_data.name)
    result = await session.execute(stmt)
    existing_genre = result.scalar_one_or_none()

    if existing_genre:
        raise HTTPException(status_code=400, detail="Genre with this name already exists")

    # Создаем новый жанр
    new_genre = Genre(**genre_data.model_dump(exclude_unset=True))
    session.add(new_genre)
    await session.commit()
    await session.refresh(new_genre)

    return GenreRead.model_validate(new_genre)


@router.get("", response_model=list[GenreRead], summary="Список жанров")
async def list_genres_admin(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех жанров (только для суперпользователя)"""
    stmt = select(Genre).order_by(Genre.name)
    result = await session.execute(stmt)
    genres = result.scalars().all()

    return [GenreRead.model_validate(genre) for genre in genres]


@router.get("/{genre_id}", response_model=GenreRead, summary="Детали жанра")
async def get_genre_admin(
    genre_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали жанра по ID (только для суперпользователя)"""
    stmt = select(Genre).where(Genre.id == genre_id)
    result = await session.execute(stmt)
    genre = result.scalar_one_or_none()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    return GenreRead.model_validate(genre)


@router.put("/{genre_id}", response_model=GenreRead, summary="Обновить жанр")
async def update_genre_admin(
    genre_id: int,
    genre_data: GenreUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить жанр (только для суперпользователя)"""
    stmt = select(Genre).where(Genre.id == genre_id)
    result = await session.execute(stmt)
    genre = result.scalar_one_or_none()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Проверяем, не существует ли другой жанр с таким названием
    check_stmt = select(Genre).where(Genre.name == genre_data.name, Genre.id != genre_id)
    check_result = await session.execute(check_stmt)
    existing_genre = check_result.scalar_one_or_none()

    if existing_genre:
        raise HTTPException(status_code=400, detail="Genre with this name already exists")

    # Обновляем поля жанра
    update_data = genre_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(genre, field, value)

    await session.commit()
    await session.refresh(genre)

    return GenreRead.model_validate(genre)


@router.delete("/{genre_id}", response_model=OperationResponse, summary="Удалить жанр")
async def delete_genre_admin(
    genre_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить жанр (только для суперпользователя)"""
    stmt = select(Genre).where(Genre.id == genre_id)
    result = await session.execute(stmt)
    genre = result.scalar_one_or_none()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    await session.delete(genre)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Genre deleted successfully",
        id=genre_id
    )

