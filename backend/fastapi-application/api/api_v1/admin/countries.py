from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import db_helper, Country
from core.schemas import (
    CountryRead,
    CountryCreate,
    CountryUpdate,
    OperationResponse,
)
from api.api_v1.fastapi_users import current_active_superuser

router = APIRouter(
    prefix="/countries",
    dependencies=[Depends(current_active_superuser)],
)


@router.post("", response_model=CountryRead, summary="Создать страну")
async def create_country(
    country_data: CountryCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новую страну (только для суперпользователя)"""
    # Проверяем, существует ли страна с таким названием
    stmt = select(Country).where(Country.name == country_data.name)
    result = await session.execute(stmt)
    existing_country = result.scalar_one_or_none()

    if existing_country:
        raise HTTPException(status_code=400, detail="Country with this name already exists")

    # Создаем новую страну
    new_country = Country(**country_data.model_dump(exclude_unset=True))
    session.add(new_country)
    await session.commit()
    await session.refresh(new_country)

    return CountryRead.model_validate(new_country)


@router.get("", response_model=list[CountryRead], summary="Список стран")
async def list_countries_admin(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список всех стран (только для суперпользователя)"""
    stmt = select(Country).order_by(Country.name)
    result = await session.execute(stmt)
    countries = result.scalars().all()

    return [CountryRead.model_validate(country) for country in countries]


@router.get("/{country_id}", response_model=CountryRead, summary="Детали страны")
async def get_country_admin(
    country_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить детали страны по ID (только для суперпользователя)"""
    stmt = select(Country).where(Country.id == country_id)
    result = await session.execute(stmt)
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return CountryRead.model_validate(country)


@router.put("/{country_id}", response_model=CountryRead, summary="Обновить страну")
async def update_country_admin(
    country_id: int,
    country_data: CountryUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить страну (только для суперпользователя)"""
    stmt = select(Country).where(Country.id == country_id)
    result = await session.execute(stmt)
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # Проверяем, не существует ли другая страна с таким названием
    check_stmt = select(Country).where(Country.name == country_data.name, Country.id != country_id)
    check_result = await session.execute(check_stmt)
    existing_country = check_result.scalar_one_or_none()

    if existing_country:
        raise HTTPException(status_code=400, detail="Country with this name already exists")

    # Обновляем поля страны
    update_data = country_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(country, field, value)

    await session.commit()
    await session.refresh(country)

    return CountryRead.model_validate(country)


@router.delete("/{country_id}", response_model=OperationResponse, summary="Удалить страну")
async def delete_country_admin(
    country_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить страну (только для суперпользователя)"""
    stmt = select(Country).where(Country.id == country_id)
    result = await session.execute(stmt)
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    await session.delete(country)
    await session.commit()

    return OperationResponse(
        status="success",
        message="Country deleted successfully",
        id=country_id
    )

