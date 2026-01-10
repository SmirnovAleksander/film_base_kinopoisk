from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.models import db_helper, Stuff
from core.models.associations import content_stuff
from core.schemas import (
    ContentStuffRead,
    ContentStuffCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/content-stuff",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/content-stuff - Сопоставить актера или режиссера с контентом и его ролью
@router.post("", response_model=ContentStuffRead, summary="Создать связь контент-участник")
async def create_content_stuff_admin(
    csi_data: ContentStuffCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать связь между контентом и участником (только для суперпользователя)"""
    # Проверяем, что участник существует
    stuff_stmt = select(Stuff).where(Stuff.id == csi_data.stuff_id)
    stuff_result = await session.execute(stuff_stmt)
    stuff = stuff_result.scalar_one_or_none()
    
    if not stuff:
        raise HTTPException(status_code=404, detail="Stuff not found")
    
    # Проверяем, не существует ли уже такая связь с той же ролью
    check_stmt = select(content_stuff).where(
        content_stuff.c.content_id == csi_data.content_id,
        content_stuff.c.content_type == csi_data.content_type,
        content_stuff.c.stuff_id == csi_data.stuff_id,
        content_stuff.c.role == csi_data.role
    )
    check_result = await session.execute(check_stmt)
    existing = check_result.first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Content-Stuff association already exists")
    
    # Создаем связь
    insert_stmt = insert(content_stuff).values(
        content_id=csi_data.content_id,
        content_type=csi_data.content_type,
        stuff_id=csi_data.stuff_id,
        role=csi_data.role
    ).returning(content_stuff.c.id, content_stuff.c.content_id, content_stuff.c.content_type, content_stuff.c.stuff_id, content_stuff.c.role)
    
    result = await session.execute(insert_stmt)
    await session.commit()
    
    row = result.first()
    return ContentStuffRead(
        id=row.id,
        content_id=row.content_id,
        content_type=row.content_type,
        stuff_id=row.stuff_id,
        role=row.role
    )


# GET /api/v1/admin/content-stuff?content_id=1 - Список всех участников проекта с их ролями
@router.get("", response_model=list[ContentStuffRead], summary="Список связей контент-участник")
async def list_content_stuff_admin(
    content_id: Optional[int] = Query(None, description="Фильтр по ID контента"),
    content_type: Optional[str] = Query(None, description="Фильтр по типу контента"),
    stuff_id: Optional[int] = Query(None, description="Фильтр по ID участника"),
    role: Optional[str] = Query(None, description="Фильтр по роли"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список связей контент-участник (только для суперпользователя)"""
    stmt = select(content_stuff)
    
    conditions = []
    if content_id:
        conditions.append(content_stuff.c.content_id == content_id)
    if content_type:
        conditions.append(content_stuff.c.content_type == content_type)
    if stuff_id:
        conditions.append(content_stuff.c.stuff_id == stuff_id)
    if role:
        conditions.append(content_stuff.c.role == role)
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    result = await session.execute(stmt)
    rows = result.all()
    
    return [
        ContentStuffRead(
            id=row.id,
            content_id=row.content_id,
            content_type=row.content_type,
            stuff_id=row.stuff_id,
            role=row.role
        )
        for row in rows
    ]


# GET /api/v1/admin/content-stuff/1 - Просмотр деталей участия человека в проекте
@router.get("/{association_id}", response_model=ContentStuffRead, summary="Детали связи контент-участник")
async def get_content_stuff_admin(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали связи по ID (только для суперпользователя)"""
    stmt = select(content_stuff).where(content_stuff.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Content-Stuff association not found")
    
    return ContentStuffRead(
        id=row.id,
        content_id=row.content_id,
        content_type=row.content_type,
        stuff_id=row.stuff_id,
        role=row.role
    )


# DELETE /api/v1/admin/content-stuff/1 - Удалить запись об участии человека в фильме/сериале
@router.delete("/{association_id}", response_model=OperationResponse, summary="Удалить связь контент-участник")
async def delete_content_stuff_admin(
    association_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить связь контент-участник (только для суперпользователя)"""
    stmt = select(content_stuff).where(content_stuff.c.id == association_id)
    result = await session.execute(stmt)
    row = result.first()
    
    if not row:
        raise HTTPException(status_code=404, detail="Content-Stuff association not found")
    
    delete_stmt = delete(content_stuff).where(content_stuff.c.id == association_id)
    await session.execute(delete_stmt)
    await session.commit()
    
    return OperationResponse(
        status="success",
        message="Content-Stuff association deleted successfully",
        id=association_id
    )
