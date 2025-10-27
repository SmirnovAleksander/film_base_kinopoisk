from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.models import db_helper, Stuff
from core.schemas import (
    StuffRead,
    StuffCreate,
    StuffUpdate,
    OperationResponse,
    StuffListResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/stuff",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=StuffRead, summary="Создать актера")
async def create_stuff(
    stuff_data: StuffCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать нового актера (только для суперпользователя)"""
    # Проверяем, существует ли актер с таким kinopoisk_id
    stmt = select(Stuff).where(Stuff.kinopoisk_id == stuff_data.kinopoisk_id)
    result = await session.execute(stmt)
    existing_stuff = result.scalar_one_or_none()

    if existing_stuff:
        raise HTTPException(status_code=400, detail="Stuff with this kinopoisk_id already exists")

    # Создаем нового актера
    new_stuff = Stuff(**stuff_data.model_dump(exclude_unset=True))
    session.add(new_stuff)
    await session.commit()
    await session.refresh(new_stuff)

    return StuffRead.model_validate(new_stuff)


@router.get("", response_model=StuffListResponse, summary="Список актеров")
async def list_stuff_admin(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(50, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех актеров с пагинацией (только для суперпользователя)"""
    offset = (page - 1) * page_size

    # Получаем общее количество актеров
    total_count_stmt = select(func.count(Stuff.id))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()

    # Получаем актеров для текущей страницы
    stmt = (
        select(Stuff)
        .order_by(Stuff.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    stuff_list = result.scalars().all()

    items = [StuffRead.model_validate(stuff) for stuff in stuff_list]

    return StuffListResponse(
        items=items,
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


@router.get("/{stuff_id}", response_model=StuffRead, summary="Детали актера")
async def get_stuff_admin(
    stuff_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали актера по ID (только для суперпользователя)"""
    stmt = select(Stuff).where(Stuff.id == stuff_id)
    result = await session.execute(stmt)
    stuff = result.scalar_one_or_none()

    if not stuff:
        raise HTTPException(status_code=404, detail="Stuff not found")

    return StuffRead.model_validate(stuff)


@router.put("/{stuff_id}", response_model=StuffRead, summary="Обновить актера")
async def update_stuff_admin(
    stuff_id: int,
    stuff_data: StuffUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить актера (только для суперпользователя)"""
    stmt = select(Stuff).where(Stuff.id == stuff_id)
    result = await session.execute(stmt)
    stuff = result.scalar_one_or_none()

    if not stuff:
        raise HTTPException(status_code=404, detail="Stuff not found")

    # Обновляем поля актера
    update_data = stuff_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stuff, field, value)

    await session.commit()
    await session.refresh(stuff)

    return StuffRead.model_validate(stuff)


@router.delete("/{stuff_id}", response_model=OperationResponse, summary="Удалить актера")
async def delete_stuff_admin(
    stuff_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить актера (только для суперпользователя)"""
    stmt = select(Stuff).where(Stuff.id == stuff_id)
    result = await session.execute(stmt)
    stuff = result.scalar_one_or_none()

    if not stuff:
        raise HTTPException(status_code=404, detail="Stuff not found")

    await session.delete(stuff)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Stuff deleted successfully",
        id=stuff_id
    )
