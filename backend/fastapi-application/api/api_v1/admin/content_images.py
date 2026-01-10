from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, ContentImage
from core.schemas import (
    ContentImageRead,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/content-images",
    dependencies=[Depends(current_active_superuser)],
)

ALLOWED_TYPES = {"stills", "wall", "shooting", "screenshots"}


# GET /api/v1/admin/content-images?content_id=1&content_type=film - Список всех изображений (кадры, обои) по фильтрам
@router.get("", response_model=list[ContentImageRead], summary="Список изображений контента")
async def list_content_images_admin(
    content_id: int | None = Query(None, description="ID контента"),
    content_type: str | None = Query(None, description="Тип контента (film/series)"),
    image_type: str | None = Query(None, description="Тип изображения"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех изображений контента (только для суперпользователя)"""
    stmt = select(ContentImage).order_by(ContentImage.id.desc())
    
    conditions = []
    if content_id is not None:
        conditions.append(ContentImage.content_id == content_id)
    if content_type is not None:
        conditions.append(ContentImage.content_type == content_type)
    if image_type is not None:
        conditions.append(ContentImage.image_type == image_type)
        
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    images = result.scalars().all()

    return [ContentImageRead.model_validate(img) for img in images]


# GET /api/v1/admin/content-images/1 - Детальная информация о конкретном изображении по ID
@router.get("/{image_id}", response_model=ContentImageRead, summary="Детали изображения")
async def get_content_image_admin(
    image_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали изображения по ID (только для суперпользователя)"""
    stmt = select(ContentImage).where(ContentImage.id == image_id)
    result = await session.execute(stmt)
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return ContentImageRead.model_validate(image)


# DELETE /api/v1/admin/content-images/1 - Удалить изображение из базы данных
@router.delete("/{image_id}", response_model=OperationResponse, summary="Удалить изображение")
async def delete_content_image_admin(
    image_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить изображение (только для суперпользователя)"""
    stmt = select(ContentImage).where(ContentImage.id == image_id)
    result = await session.execute(stmt)
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    await session.delete(image)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Image deleted successfully",
        id=image_id,
    )
