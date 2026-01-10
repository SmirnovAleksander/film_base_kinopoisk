from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, ContentWatchProvider
from core.schemas import (
    ContentWatchProviderRead,
    ContentWatchProviderCreate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/content-watch-providers",
    dependencies=[Depends(current_active_superuser)],
)


# POST /api/v1/admin/content-watch-providers - Привязать онлайн-кинотеатр к фильму или сериалу
@router.post("", response_model=ContentWatchProviderRead, summary="Создать провайдера просмотра")
async def create_watch_provider_admin(
    provider_data: ContentWatchProviderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать запись о провайдере просмотра (только для суперпользователя)"""
    dup_stmt = select(ContentWatchProvider).where(
        ContentWatchProvider.content_id == provider_data.content_id,
        ContentWatchProvider.content_type == provider_data.content_type,
        ContentWatchProvider.provider_name == provider_data.provider_name,
    )
    dup_result = await session.execute(dup_stmt)
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=400, detail="Watch provider already exists for this content")

    provider = ContentWatchProvider(**provider_data.model_dump(exclude_unset=True))
    session.add(provider)
    await session.commit()
    await session.refresh(provider)

    return ContentWatchProviderRead.model_validate(provider)


# GET /api/v1/admin/content-watch-providers?content_id=1 - Список всех привязок к онлайн-кинотеатрам
@router.get("", response_model=list[ContentWatchProviderRead], summary="Список провайдеров просмотра")
async def list_watch_providers_admin(
    content_id: int | None = Query(None, description="ID контента"),
    content_type: str | None = Query(None, description="Тип контента (film/series)"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех провайдеров просмотра (только для суперпользователя)"""
    stmt = select(ContentWatchProvider).order_by(ContentWatchProvider.id.desc())
    
    conditions = []
    if content_id is not None:
        conditions.append(ContentWatchProvider.content_id == content_id)
    if content_type is not None:
        conditions.append(ContentWatchProvider.content_type == content_type)
        
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    providers = result.scalars().all()

    return [ContentWatchProviderRead.model_validate(provider) for provider in providers]


# GET /api/v1/admin/content-watch-providers/1 - Получить данные о конкретной привязке контента к площадке
@router.get("/{provider_id}", response_model=ContentWatchProviderRead, summary="Детали провайдера")
async def get_watch_provider_admin(
    provider_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали провайдера просмотра по ID (только для суперпользователя)"""
    stmt = select(ContentWatchProvider).where(ContentWatchProvider.id == provider_id)
    result = await session.execute(stmt)
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(status_code=404, detail="Watch provider not found")

    return ContentWatchProviderRead.model_validate(provider)


# DELETE /api/v1/admin/content-watch-providers/1 - Удалить привязку фильма/сериала к онлайн-площадке
@router.delete("/{provider_id}", response_model=OperationResponse, summary="Удалить провайдера")
async def delete_watch_provider_admin(
    provider_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить провайдера просмотра (только для суперпользователя)"""
    stmt = select(ContentWatchProvider).where(ContentWatchProvider.id == provider_id)
    result = await session.execute(stmt)
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(status_code=404, detail="Watch provider not found")

    await session.delete(provider)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Watch provider deleted successfully",
        id=provider_id,
    )
