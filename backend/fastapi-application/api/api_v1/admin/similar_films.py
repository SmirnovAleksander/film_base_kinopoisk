from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, SimilarFilm, Film
from core.schemas import (
    SimilarFilmRead,
    SimilarFilmCreate,
    SimilarFilmUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/similar-films",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=SimilarFilmRead, summary="Создать похожий фильм")
async def create_similar_film(
    similar_film_data: SimilarFilmCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать запись о похожем фильме (только для суперпользователя)"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == similar_film_data.film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    # Проверяем дубликаты
    stmt = select(SimilarFilm).where(
        SimilarFilm.film_id == similar_film_data.film_id,
        SimilarFilm.similar_film_id == similar_film_data.similar_film_id,
    )
    result = await session.execute(stmt)
    existing_similar = result.scalar_one_or_none()

    if existing_similar:
        raise HTTPException(status_code=400, detail="Similar film already exists for this film")

    new_similar = SimilarFilm(**similar_film_data.model_dump(exclude_unset=True))
    session.add(new_similar)
    await session.commit()
    await session.refresh(new_similar)

    return SimilarFilmRead.model_validate(new_similar)


@router.get("", response_model=list[SimilarFilmRead], summary="Список похожих фильмов")
async def list_similar_films_admin(
    film_id: int | None = Query(None, description="Фильтр по ID фильма"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список похожих фильмов (только для суперпользователя)"""
    stmt = select(SimilarFilm).order_by(SimilarFilm.id.desc())
    if film_id is not None:
        stmt = stmt.where(SimilarFilm.film_id == film_id)

    result = await session.execute(stmt)
    items = result.scalars().all()

    return [SimilarFilmRead.model_validate(item) for item in items]


@router.get("/{similar_film_id}", response_model=SimilarFilmRead, summary="Детали похожего фильма")
async def get_similar_film_admin(
    similar_film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали похожего фильма по ID (только для суперпользователя)"""
    stmt = select(SimilarFilm).where(SimilarFilm.id == similar_film_id)
    result = await session.execute(stmt)
    similar_film = result.scalar_one_or_none()

    if not similar_film:
        raise HTTPException(status_code=404, detail="Similar film not found")

    return SimilarFilmRead.model_validate(similar_film)


@router.put("/{similar_film_id}", response_model=SimilarFilmRead, summary="Обновить похожий фильм")
async def update_similar_film_admin(
    similar_film_id: int,
    similar_film_data: SimilarFilmUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить запись о похожем фильме (только для суперпользователя)"""
    stmt = select(SimilarFilm).where(SimilarFilm.id == similar_film_id)
    result = await session.execute(stmt)
    similar_film = result.scalar_one_or_none()

    if not similar_film:
        raise HTTPException(status_code=404, detail="Similar film not found")

    # Если передан film_id, проверяем, что фильм существует
    if similar_film_data.film_id is not None:
        film_stmt = select(Film).where(Film.id == similar_film_data.film_id)
        film_result = await session.execute(film_stmt)
        film = film_result.scalar_one_or_none()
        if not film:
            raise HTTPException(status_code=404, detail="Film not found")

    # Проверяем уникальность пары film_id + similar_film_id
    new_film_id = similar_film_data.film_id or similar_film.film_id
    new_similar_id = similar_film_data.similar_film_id or similar_film.similar_film_id

    dup_stmt = select(SimilarFilm).where(
        SimilarFilm.film_id == new_film_id,
        SimilarFilm.similar_film_id == new_similar_id,
        SimilarFilm.id != similar_film_id,
    )
    dup_result = await session.execute(dup_stmt)
    duplicate = dup_result.scalar_one_or_none()

    if duplicate:
        raise HTTPException(status_code=400, detail="Similar film already exists for this film")

    update_data = similar_film_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(similar_film, field, value)

    await session.commit()
    await session.refresh(similar_film)

    return SimilarFilmRead.model_validate(similar_film)


@router.delete("/{similar_film_id}", response_model=OperationResponse, summary="Удалить похожий фильм")
async def delete_similar_film_admin(
    similar_film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить запись о похожем фильме (только для суперпользователя)"""
    stmt = select(SimilarFilm).where(SimilarFilm.id == similar_film_id)
    result = await session.execute(stmt)
    similar_film = result.scalar_one_or_none()

    if not similar_film:
        raise HTTPException(status_code=404, detail="Similar film not found")

    await session.delete(similar_film)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Similar film deleted successfully",
        id=similar_film_id,
    )


