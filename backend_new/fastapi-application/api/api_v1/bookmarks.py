from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import db_helper, Bookmark, Film, User
from core.schemas import BookmarkResponse, BookmarkStatusResponse
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


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
        .options(selectinload(Bookmark.film))
        .where(Bookmark.user_id == user.id)
        .order_by(Bookmark.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    bookmarks = result.scalars().all()
    
    return BookmarkResponse(
        items=[
            {
                "id": bookmark.id,
                "user_id": bookmark.user_id,
                "film_id": bookmark.film_id,
                "created_at": bookmark.created_at,
                "film": {
                    "id": bookmark.film.id,
                    "kinopoisk_id": bookmark.film.kinopoisk_id,
                    "title": bookmark.film.title,
                    "original_title": bookmark.film.original_title,
                    "description": bookmark.film.description,
                    "full_description": bookmark.film.full_description,
                    "poster": bookmark.film.poster,
                    "year": bookmark.film.year,
                    "tagline": bookmark.film.tagline,
                    "ru_premiere": bookmark.film.ru_premiere,
                    "world_premiere": bookmark.film.world_premiere,
                    "content_rating": bookmark.film.content_rating,
                    "is_family_friendly": bookmark.film.is_family_friendly,
                    "duration": bookmark.film.duration,
                    "rating_kp": bookmark.film.rating_kp,
                    "kp_votes_count": bookmark.film.kp_votes_count,
                    "rating_imdb": bookmark.film.rating_imdb,
                    "imdb_votes_count": bookmark.film.imdb_votes_count,
                    "user_rating": bookmark.film.user_rating,
                    "user_rating_count": bookmark.film.user_rating_count,
                    "budget": bookmark.film.budget,
                    "usa_box_office": bookmark.film.usa_box_office,
                    "rus_box_office": bookmark.film.rus_box_office,
                } if bookmark.film else None
            }
            for bookmark in bookmarks
        ],
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )


@router.post("/{film_id}", summary="Добавить фильм в закладки")
async def add_bookmark(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Добавить фильм в закладки"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Проверяем, есть ли уже закладка
    existing_stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.film_id == film_id
    )
    existing_result = await session.execute(existing_stmt)
    existing_bookmark = existing_result.scalar_one_or_none()
    
    if existing_bookmark:
        return {"status": "already_exists"}
    
    # Создаем новую закладку
    bookmark = Bookmark(user_id=user.id, film_id=film_id)
    session.add(bookmark)
    await session.commit()
    await session.refresh(bookmark)
    
    return {"status": "added", "bookmark_id": bookmark.id}


@router.delete("/{film_id}", summary="Удалить фильм из закладок")
async def remove_bookmark(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить фильм из закладок"""
    stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.film_id == film_id
    )
    result = await session.execute(stmt)
    bookmark = result.scalar_one_or_none()
    
    if not bookmark:
        return {"status": "not_found"}
    
    await session.delete(bookmark)
    await session.commit()
    
    return {"status": "removed"}


@router.get("/{film_id}/status", response_model=BookmarkStatusResponse, summary="Проверить статус закладки")
async def check_bookmark_status(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Проверить статус закладки для фильма"""
    stmt = select(Bookmark).where(
        Bookmark.user_id == user.id,
        Bookmark.film_id == film_id
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
