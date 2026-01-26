from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.models import db_helper, Series
from core.schemas import (
    SeriesRead,
    SeriesBase,
    SeriesUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/series",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/series - Добавить новую запись о сериале
@router.post("", response_model=SeriesRead, summary="Создать сериал")
async def create_series(
    series_data: SeriesBase,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новый сериал (только для суперпользователя)"""
    stmt = select(Series).where(Series.kinopoisk_id == series_data.kinopoisk_id)
    result = await session.execute(stmt)
    existing_series = result.scalar_one_or_none()

    if existing_series:
        raise HTTPException(status_code=400, detail="Series with this kinopoisk_id already exists")

    new_series = Series(**series_data.model_dump(exclude_unset=True))
    session.add(new_series)
    await session.commit()
    
    # Перезагружаем со связями
    stmt = select(Series).options(selectinload(Series.user_rating)).where(Series.id == new_series.id)
    new_series = (await session.execute(stmt)).scalar_one()

    return SeriesRead.model_validate(new_series)


# GET /api/v1/admin/series - Список всех сериалов в базе с пагинацией
@router.get("", response_model=list[SeriesRead], summary="Список сериалов")
async def list_series_admin(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(50, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех сериалов с пагинацией (только для суперпользователя)"""
    offset = (page - 1) * page_size

    stmt = (
        select(Series)
        .options(selectinload(Series.user_rating))
        .order_by(Series.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    series_list = result.scalars().all()

    return [SeriesRead.model_validate(series) for series in series_list]


# GET /api/v1/admin/series/1 - Просмотр технических данных сериала по ID
@router.get("/{series_id}", response_model=SeriesRead, summary="Детали сериала")
async def get_series_admin(
    series_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали сериала по ID (только для суперпользователя)"""
    stmt = select(Series).options(selectinload(Series.user_rating)).where(Series.id == series_id)
    result = await session.execute(stmt)
    series = result.scalar_one_or_none()

    if not series:
        raise HTTPException(status_code=404, detail="Series not found")

    return SeriesRead.model_validate(series)


# PUT /api/v1/admin/series/1 - Обновить информацию о существующем сериале
@router.put("/{series_id}", response_model=SeriesRead, summary="Обновить сериал")
async def update_series_admin(
    series_id: int,
    series_data: SeriesUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить сериал (только для суперпользователя)"""
    stmt = select(Series).options(selectinload(Series.user_rating)).where(Series.id == series_id)
    result = await session.execute(stmt)
    series = result.scalar_one_or_none()

    if not series:
        raise HTTPException(status_code=404, detail="Series not found")

    update_data = series_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(series, field, value)

    await session.commit()
    
    # Перезагружаем со связями
    stmt = select(Series).options(selectinload(Series.user_rating)).where(Series.id == series_id)
    series = (await session.execute(stmt)).scalar_one()

    return SeriesRead.model_validate(series)


# DELETE /api/v1/admin/series/1 - Удалить сериал из базы данных
@router.delete("/{series_id}", response_model=OperationResponse, summary="Удалить сериал")
async def delete_series_admin(
    series_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить сериал (только для суперпользователя)"""
    stmt = select(Series).where(Series.id == series_id)
    result = await session.execute(stmt)
    series = result.scalar_one_or_none()

    if not series:
        raise HTTPException(status_code=404, detail="Series not found")

    await session.delete(series)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Series deleted successfully",
        id=series_id
    )
