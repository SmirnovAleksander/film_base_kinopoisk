from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import db_helper, Genre
from core.schemas import GenreRead

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


@router.get("", response_model=List[GenreRead], summary="Все жанры")
async def list_genres(session: AsyncSession = Depends(db_helper.session_getter)):
    """Получить список всех жанров"""
    stmt = select(Genre).order_by(Genre.name)
    result = await session.execute(stmt)
    genres = result.scalars().all()
    
    return [GenreRead.model_validate(genre) for genre in genres]
