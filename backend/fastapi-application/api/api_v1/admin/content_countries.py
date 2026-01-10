from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.models import db_helper, Country
from core.models.associations import content_country
from core.schemas import (
    ContentCountryRead,
    ContentCountryCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/content-countries",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/content-countries - Привязать страну производства к фильму или сериалу
@router.post("", response_model=ContentCountryRead, summary="Создать связь контент-страна")
async def create_content_country_admin(
    cci_data: ContentCountryCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь между контентом и страной (только для суперпользователя)"""
    # Проверяем, что страна существует
    country_stmt = select(Country).where(Country.id == cci_data.country_id)
    country_result = await session.execute(country_stmt)
    country = country_result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    # Проверяем, не существует ли уже такая связь
    check_stmt = select(content_country).where(
        content_country.c.content_id == cci_data.content_id,
        content_country.c.content_type == cci_data.content_type,
        content_country.c.country_id == cci_data.country_id
    )
    check_result = await session.execute(check_stmt)
    existing = check_result.first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Content-Country association already exists")
    
    # Создаем связь
    insert_stmt = insert(content_country).values(
        content_id=cci_data.content_id,
        content_type=cci_data.content_type,
        country_id=cci_data.country_id
    ).returning(content_country.c.id, content_country.c.content_id, content_country.c.content_type, content_country.c.country_id)
    
    result = await session.execute(insert_stmt)
    await session.commit()
    
    row = result.first()
    return ContentCountryRead(
        id=row.id,
        content_id=row.content_id,
        content_type=row.content_type,
        country_id=row.country_id
    )


# GET /api/v1/admin/content-countries?content_id=1 - Список всех привязок стран к контенту
@router.get("", response_model=list[ContentCountryRead], summary="Список связей контент-страна")
async def list_content_countries_admin(
    content_id: Optional[int] = Query(None, description="Фильтр по ID контента"),
    content_type: Optional[str] = Query(None, description="Фильтр по типу контента"),
    country_id: Optional[int] = Query(None, description="Фильтр по ID страны"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список связей контент-страна (только для суперпользователя)"""
    stmt = select(content_country)
    
    conditions = []
    if content_id:
        conditions.append(content_country.c.content_id == content_id)
    if content_type:
        conditions.append(content_country.c.content_type == content_type)
    if country_id:
        conditions.append(content_country.c.country_id == country_id)
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    result = await session.execute(stmt)
    rows = result.all()
    
    return [
        ContentCountryRead(
            id=row.id,
            content_id=row.content_id,
            content_type=row.content_type,
            country_id=row.country_id
        )
        for row in rows
    ]


# GET /api/v1/admin/content-countries/1 - Информация о конкретной записи привязки страны
@router.get("/{association_id}", response_model=ContentCountryRead, summary="Детали связи контент-страна")
async def get_content_country_admin(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи по ID (только для суперпользователя)"""
    stmt = select(content_country).where(content_country.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Content-Country association not found")
    
    return ContentCountryRead(
        id=row.id,
        content_id=row.content_id,
        content_type=row.content_type,
        country_id=row.country_id
    )


# DELETE /api/v1/admin/content-countries/1 - Удалить связь фильма/сериала со страной
@router.delete("/{association_id}", response_model=OperationResponse, summary="Удалить связь контент-страна")
async def delete_content_country_admin(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь контент-страна (только для суперпользователя)"""
    stmt = select(content_country).where(content_country.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Content-Country association not found")
    
    delete_stmt = delete(content_country).where(content_country.c.id == association_id)
    await session.execute(delete_stmt)
    await session.commit()
    
    return OperationResponse(
        status="success",
        message="Content-Country association deleted successfully",
        id=association_id
    )
