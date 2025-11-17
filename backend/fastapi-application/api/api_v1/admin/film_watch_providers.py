from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Film, FilmWatchProvider
from core.schemas import (
    FilmWatchProviderRead,
    FilmWatchProviderCreate,
    FilmWatchProviderUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/film-watch-providers",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=FilmWatchProviderRead, summary="Создать провайдера просмотра фильма")
async def create_watch_provider(
    provider_data: FilmWatchProviderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать запись о провайдере просмотра фильма (только для суперпользователя)"""
    film_stmt = select(Film).where(Film.id == provider_data.film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    dup_stmt = select(FilmWatchProvider).where(
        FilmWatchProvider.film_id == provider_data.film_id,
        FilmWatchProvider.name == provider_data.name,
    )
    dup_result = await session.execute(dup_stmt)
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=400, detail="Watch provider already exists for this film")

    provider = FilmWatchProvider(**provider_data.model_dump(exclude_unset=True))
    session.add(provider)
    await session.commit()
    await session.refresh(provider)

    return FilmWatchProviderRead.model_validate(provider)


@router.get("", response_model=list[FilmWatchProviderRead], summary="Список провайдеров просмотра")
async def list_watch_providers_admin(
    film_id: int | None = Query(None, description="Фильтр по ID фильма"),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список провайдеров просмотра (только для суперпользователя)"""
    stmt = select(FilmWatchProvider).order_by(FilmWatchProvider.id.desc())
    if film_id is not None:
        stmt = stmt.where(FilmWatchProvider.film_id == film_id)

    result = await session.execute(stmt)
    providers = result.scalars().all()

    return [FilmWatchProviderRead.model_validate(provider) for provider in providers]


@router.get("/{provider_id}", response_model=FilmWatchProviderRead, summary="Детали провайдера просмотра")
async def get_watch_provider_admin(
    provider_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали провайдера просмотра по ID (только для суперпользователя)"""
    stmt = select(FilmWatchProvider).where(FilmWatchProvider.id == provider_id)
    result = await session.execute(stmt)
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(status_code=404, detail="Watch provider not found")

    return FilmWatchProviderRead.model_validate(provider)


@router.put("/{provider_id}", response_model=FilmWatchProviderRead, summary="Обновить провайдера просмотра")
async def update_watch_provider_admin(
    provider_id: int,
    provider_data: FilmWatchProviderUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить запись о провайдере просмотра (только для суперпользователя)"""
    stmt = select(FilmWatchProvider).where(FilmWatchProvider.id == provider_id)
    result = await session.execute(stmt)
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(status_code=404, detail="Watch provider not found")

    if provider_data.film_id is not None:
        film_stmt = select(Film).where(Film.id == provider_data.film_id)
        film_result = await session.execute(film_stmt)
        film = film_result.scalar_one_or_none()
        if not film:
            raise HTTPException(status_code=404, detail="Film not found")

    new_film_id = provider_data.film_id or provider.film_id
    new_name = provider_data.name or provider.name

    dup_stmt = select(FilmWatchProvider).where(
        FilmWatchProvider.film_id == new_film_id,
        FilmWatchProvider.name == new_name,
        FilmWatchProvider.id != provider_id,
    )
    dup_result = await session.execute(dup_stmt)
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=400, detail="Watch provider already exists for this film")

    update_data = provider_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(provider, field, value)

    await session.commit()
    await session.refresh(provider)

    return FilmWatchProviderRead.model_validate(provider)


@router.delete("/{provider_id}", response_model=OperationResponse, summary="Удалить провайдера просмотра")
async def delete_watch_provider_admin(
    provider_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить провайдера просмотра фильма (только для суперпользователя)"""
    stmt = select(FilmWatchProvider).where(FilmWatchProvider.id == provider_id)
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


