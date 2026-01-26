from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import db_helper, Country
from core.schemas import CountryRead

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


@router.get("", response_model=List[CountryRead], summary="Все страны")
async def list_countries(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить список всех стран"""
    stmt = select(Country).order_by(Country.name)
    result = await session.execute(stmt)
    countries = result.scalars().all()
    
    return [CountryRead.model_validate(country) for country in countries]
