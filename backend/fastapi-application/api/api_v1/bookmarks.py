from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.models import ( 
    db_helper, 
    Bookmark, 
    Film, 
    Series,
    User 
)
from core.schemas import (
    BookmarkResponse,
    BookmarkStatusResponse,
    BookmarkRead,
    FilmRead,
    SeriesRead,
    BookmarkOperationResponse,
)
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


# GET /api/v1/bookmarks/ - Получить список всех закладок (фильмов и сериалов) текущего пользователя
@router.get("/", response_model=BookmarkResponse, summary="Список закладок пользователя")
async def list_bookmarks(
    page: int = 1,
    page_size: int = 20,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список закладок пользователя"""
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    
    offset = (page - 1) * page_size
    
    # Получаем общее количество закладок пользователя
    total_count_stmt = select(func.count(Bookmark.id)).where(Bookmark.user_id == user.id)
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    stmt = (
        select(Bookmark)
        .options(selectinload(Bookmark.film), selectinload(Bookmark.series))
        .where(Bookmark.user_id == user.id)
        .order_by(Bookmark.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    bookmarks = result.scalars().all()
    
    items = []
    for bookmark in bookmarks:
        film_data = FilmRead.model_validate(bookmark.film) if bookmark.content_type == "film" and bookmark.film else None
        series_data = SeriesRead.model_validate(bookmark.series) if bookmark.content_type == "series" and bookmark.series else None

        items.append(BookmarkRead(
            id=bookmark.id,
            user_id=bookmark.user_id,
            content_id=bookmark.content_id,
            content_type=bookmark.content_type,
            created_at=bookmark.created_at,
            film=film_data,
            series=series_data
        ))

    return BookmarkResponse(
        items=items,
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


# POST /api/v1/bookmarks/film/1 - Сохранить фильм или сериал в личный список закладок
@router.post("/{content_type}/{content_id}", response_model=BookmarkOperationResponse, summary="Добавить контент в закладки")
async def add_bookmark(
    content_type: str,
    content_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Добавить фильм или сериал в закладки"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type. Must be 'film' or 'series'")
        
    # Проверяем, что контент существует
    if content_type == "film":
        stmt = select(Film).where(Film.id == content_id)
    else:
        stmt = select(Series).where(Series.id == content_id)
        
    result = await session.execute(stmt)
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail=f"{content_type.capitalize()} not found")
    
    # Проверяем, есть ли уже закладка
    existing_stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.content_id == content_id,
        Bookmark.content_type == content_type
    )
    existing_result = await session.execute(existing_stmt)
    existing_bookmark = existing_result.scalar_one_or_none()
    
    if existing_bookmark:
        return BookmarkOperationResponse(status="already_exists")
    
    # Создаем новую закладку
    bookmark = Bookmark(user_id=user.id, content_id=content_id, content_type=content_type)
    session.add(bookmark)
    await session.commit()
    await session.refresh(bookmark)
    
    return BookmarkOperationResponse(status="added", bookmark_id=bookmark.id)


# DELETE /api/v1/bookmarks/series/1 - Удалить контент из списка закладок пользователя
@router.delete("/{content_type}/{content_id}", response_model=BookmarkOperationResponse, summary="Удалить контент из закладок")
async def remove_bookmark(
    content_type: str,
    content_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить фильм или сериал из закладок"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.content_id == content_id,
        Bookmark.content_type == content_type
    )
    result = await session.execute(stmt)
    bookmark = result.scalar_one_or_none()
    
    if not bookmark:
        return BookmarkOperationResponse(status="not_found")
    
    await session.delete(bookmark)
    await session.commit()
    
    return BookmarkOperationResponse(status="removed")


# GET /api/v1/bookmarks/film/1/status - Узнать, находится ли данный контент в закладках пользователя
@router.get("/{content_type}/{content_id}/status", response_model=BookmarkStatusResponse, summary="Проверить статус закладки")
async def check_bookmark_status(
    content_type: str,
    content_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Проверить статус закладки для контента"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.content_id == content_id,
        Bookmark.content_type == content_type
    )
    result = await session.execute(stmt)
    bookmark = result.scalar_one_or_none()
    
    if bookmark:
        return BookmarkStatusResponse(
            is_bookmarked=True,
            bookmark_id=bookmark.id,
            bookmarked_at=bookmark.created_at,
        )
    else:
        return BookmarkStatusResponse(is_bookmarked=False)
