from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Film, FilmStill
from core.schemas import (
    FilmStillRead,
    FilmStillCreate,
    FilmStillUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/film-stills",
    dependencies=[Depends(current_active_superuser)],
)

ALLOWED_SOURCES = {"stills", "wall"}


@router.post("", response_model=FilmStillRead, summary="Создать кадр фильма")
async def create_film_still(
    film_still_data: FilmStillCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новый кадр фильма (только для суперпользователя)"""
    if film_still_data.source not in ALLOWED_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Allowed values: {', '.join(sorted(ALLOWED_SOURCES))}",
        )
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_still_data.film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    # Проверяем уникальность
    stmt = select(FilmStill).where(
        FilmStill.film_id == film_still_data.film_id,
        FilmStill.picture_id == film_still_data.picture_id,
        FilmStill.source == film_still_data.source,
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Film still already exists with this picture and source")

    film_still = FilmStill(**film_still_data.model_dump(exclude_unset=True))
    session.add(film_still)
    await session.commit()
    await session.refresh(film_still)

    return FilmStillRead.model_validate(film_still)


@router.get("", response_model=list[FilmStillRead], summary="Список кадров")
async def list_film_stills_admin(
    film_id: int | None = Query(None, description="Фильтр по ID фильма"),
    source: str | None = Query(None, description="Фильтр по источнику"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список кадров фильмов (только для суперпользователя)"""
    stmt = select(FilmStill).order_by(FilmStill.id.desc())
    if film_id is not None:
        stmt = stmt.where(FilmStill.film_id == film_id)
    if source is not None:
        stmt = stmt.where(FilmStill.source == source)

    result = await session.execute(stmt)
    film_stills = result.scalars().all()

    return [FilmStillRead.model_validate(still) for still in film_stills]


@router.get("/{film_still_id}", response_model=FilmStillRead, summary="Детали кадра")
async def get_film_still_admin(
    film_still_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали кадра по ID (только для суперпользователя)"""
    stmt = select(FilmStill).where(FilmStill.id == film_still_id)
    result = await session.execute(stmt)
    film_still = result.scalar_one_or_none()

    if not film_still:
        raise HTTPException(status_code=404, detail="Film still not found")

    return FilmStillRead.model_validate(film_still)


@router.put("/{film_still_id}", response_model=FilmStillRead, summary="Обновить кадр")
async def update_film_still_admin(
    film_still_id: int,
    film_still_data: FilmStillUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить кадр фильма (только для суперпользователя)"""
    stmt = select(FilmStill).where(FilmStill.id == film_still_id)
    result = await session.execute(stmt)
    film_still = result.scalar_one_or_none()

    if not film_still:
        raise HTTPException(status_code=404, detail="Film still not found")

    # Если указали другой film_id, проверяем фильм
    if film_still_data.film_id is not None:
        film_stmt = select(Film).where(Film.id == film_still_data.film_id)
        film_result = await session.execute(film_stmt)
        film = film_result.scalar_one_or_none()
        if not film:
            raise HTTPException(status_code=404, detail="Film not found")

    if film_still_data.source is not None and film_still_data.source not in ALLOWED_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Allowed values: {', '.join(sorted(ALLOWED_SOURCES))}",
        )

    new_film_id = film_still_data.film_id or film_still.film_id
    new_picture_id = film_still_data.picture_id or film_still.picture_id
    new_source = film_still_data.source or film_still.source

    dup_stmt = select(FilmStill).where(
        FilmStill.film_id == new_film_id,
        FilmStill.picture_id == new_picture_id,
        FilmStill.source == new_source,
        FilmStill.id != film_still_id,
    )
    dup_result = await session.execute(dup_stmt)
    duplicate = dup_result.scalar_one_or_none()

    if duplicate:
        raise HTTPException(status_code=400, detail="Film still already exists with this picture and source")

    update_data = film_still_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(film_still, field, value)

    await session.commit()
    await session.refresh(film_still)

    return FilmStillRead.model_validate(film_still)


@router.delete("/{film_still_id}", response_model=OperationResponse, summary="Удалить кадр")
async def delete_film_still_admin(
    film_still_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить кадр фильма (только для суперпользователя)"""
    stmt = select(FilmStill).where(FilmStill.id == film_still_id)
    result = await session.execute(stmt)
    film_still = result.scalar_one_or_none()

    if not film_still:
        raise HTTPException(status_code=404, detail="Film still not found")

    await session.delete(film_still)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Film still deleted successfully",
        id=film_still_id,
    )


