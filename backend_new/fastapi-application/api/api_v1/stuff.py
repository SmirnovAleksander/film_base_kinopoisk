from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.config import settings
from core.models import db_helper, Stuff
from core.schemas import StuffRead, FilmSearchResponse

router = APIRouter(
    prefix=settings.api.v1.prefix + "/stuff",
    tags=["Stuff"],
)


@router.get("/", summary="Список участников")
async def list_stuff(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список участников с пагинацией"""
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * page_size
    
    # Получаем общее количество участников
    total_count_stmt = select(func.count(Stuff.id))
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем участников для текущей страницы
    stmt = (
        select(Stuff)
        .order_by(Stuff.id)
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    stuff_list = result.scalars().all()
    
    items = []
    for person in stuff_list:
        items.append({
            "id": person.id,
            "kinopoisk_id": person.kinopoisk_id,
            "name": person.name,
            "original_name": person.original_name,
            "image": person.image,
        })
    
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_count": total_count or 0,
    }


@router.get("/kinopoisk/{kinopoisk_id}", response_model=StuffRead, summary="Участник по Кинопоиск ID")
async def get_stuff_by_kinopoisk_id(
    kinopoisk_id: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить участника по его Кинопоиск ID"""
    stmt = select(Stuff).where(Stuff.kinopoisk_id == kinopoisk_id)
    result = await session.execute(stmt)
    person = result.scalar_one_or_none()
    
    if not person:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    return StuffRead.model_validate(person)


@router.get("/{stuff_id}", response_model=StuffRead, summary="Детали участника")
async def get_stuff(
    stuff_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали участника по ID"""
    stmt = select(Stuff).where(Stuff.id == stuff_id)
    result = await session.execute(stmt)
    person = result.scalar_one_or_none()
    
    if not person:
        raise HTTPException(status_code=404, detail="Stuff not found")
    
    return StuffRead.model_validate(person)
