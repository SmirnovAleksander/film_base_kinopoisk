from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.models import db_helper, Media
from core.schemas import (
    MediaRead,
    MediaCreate,
    MediaUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/media",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/media - Вручную добавить новость или статью в систему
@router.post("", response_model=MediaRead, summary="Создать медиа")
async def create_media(
    media_data: MediaCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новый медиа контент (только для суперпользователя)"""
    # Проверяем, существует ли медиа с таким URL (если URL указан)
    if media_data.url:
        stmt = select(Media).where(Media.url == media_data.url)
        result = await session.execute(stmt)
        existing_media = result.scalar_one_or_none()

        if existing_media:
            raise HTTPException(status_code=400, detail="Media with this URL already exists")

    # Создаем новый медиа контент
    new_media = Media(**media_data.model_dump(exclude_unset=True))
    session.add(new_media)
    await session.commit()
    await session.refresh(new_media)

    return MediaRead.model_validate(new_media)


# GET /api/v1/admin/media - Список всех медиа-записей с технической пагинацией
@router.get("", response_model=list[MediaRead], summary="Список медиа")
async def list_media_admin(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(50, ge=1, le=100, description="Размер страницы"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех медиа с пагинацией (только для суперпользователя)"""
    offset = (page - 1) * page_size

    # Получаем медиа для текущей страницы
    stmt = (
        select(Media)
        .order_by(Media.id.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    media_list = result.scalars().all()

    return [MediaRead.model_validate(media) for media in media_list]


# GET /api/v1/admin/media/1 - Получить техническую информацию о новости по ID
@router.get("/{media_id}", response_model=MediaRead, summary="Детали медиа")
async def get_media_admin(
    media_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали медиа по ID (только для суперпользователя)"""
    stmt = select(Media).where(Media.id == media_id)
    result = await session.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    return MediaRead.model_validate(media)


# PUT /api/v1/admin/media/1 - Изменить содержание новостной статьи или её метаданные
@router.put("/{media_id}", response_model=MediaRead, summary="Обновить медиа")
async def update_media_admin(
    media_id: int,
    media_data: MediaUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить медиа (только для суперпользователя)"""
    stmt = select(Media).where(Media.id == media_id)
    result = await session.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    # Проверяем, не существует ли другое медиа с таким URL (если URL указан)
    if media_data.url:
        check_stmt = select(Media).where(Media.url == media_data.url, Media.id != media_id)
        check_result = await session.execute(check_stmt)
        existing_media = check_result.scalar_one_or_none()

        if existing_media:
            raise HTTPException(status_code=400, detail="Media with this URL already exists")

    # Обновляем поля медиа
    update_data = media_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(media, field, value)

    await session.commit()
    await session.refresh(media)

    return MediaRead.model_validate(media)


# DELETE /api/v1/admin/media/1 - Удалить медиа-запись из базы данных
@router.delete("/{media_id}", response_model=OperationResponse, summary="Удалить медиа")
async def delete_media_admin(
    media_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить медиа (только для суперпользователя)"""
    stmt = select(Media).where(Media.id == media_id)
    result = await session.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    await session.delete(media)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Media deleted successfully",
        id=media_id
    )

