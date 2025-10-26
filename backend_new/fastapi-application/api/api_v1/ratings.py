from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import db_helper, UserFilmRating, Film, User
from core.schemas import (
    UserFilmRatingCreate,
    UserFilmRatingUpdate,
    UserFilmRatingRead,
    FilmRead,
    FilmAverageRatingRead,
    UserRatingsResponse,
)
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)


async def update_film_user_rating(session: AsyncSession, film_id: int):
    """Обновляет средний пользовательский рейтинг фильма"""
    # Вычисляем средний рейтинг и количество оценок
    avg_stmt = select(
        func.avg(UserFilmRating.rating),
        func.count(UserFilmRating.id)
    ).where(UserFilmRating.film_id == film_id)
    
    result = await session.execute(avg_stmt)
    avg_rating, rating_count = result.first()
    
    # Обновляем таблицу film
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if film:
        film.user_rating = avg_rating
        film.user_rating_count = rating_count or 0
        await session.commit()


@router.get("/films/{film_id}/rating", summary="Получить рейтинг пользователя для фильма")
async def get_user_film_rating(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить рейтинг текущего пользователя для указанного фильма"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Получаем рейтинг пользователя
    rating_stmt = select(UserFilmRating).where(
        and_(
            UserFilmRating.user_id == user.id,
            UserFilmRating.film_id == film_id
        )
    )
    rating_result = await session.execute(rating_stmt)
    rating = rating_result.scalar_one_or_none()
    
    if rating:
        return {
            "rating": rating.rating,
            "created_at": rating.created_at,
            "updated_at": rating.updated_at,
        }
    else:
        return {"rating": None}


@router.post("/films/{film_id}/rating", summary="Установить рейтинг для фильма")
async def set_user_film_rating(
    film_id: int,
    rating_data: UserFilmRatingCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Установить или обновить рейтинг пользователя для фильма"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Проверяем, есть ли уже рейтинг
    existing_stmt = select(UserFilmRating).where(
        and_(
            UserFilmRating.user_id == user.id,
            UserFilmRating.film_id == film_id
        )
    )
    existing_result = await session.execute(existing_stmt)
    existing_rating = existing_result.scalar_one_or_none()
    
    if existing_rating:
        # Обновляем существующий рейтинг
        existing_rating.rating = rating_data.rating
        await session.commit()
        await session.refresh(existing_rating)
        
        # Обновляем средний рейтинг фильма
        await update_film_user_rating(session, film_id)
        
        return {
            "rating": existing_rating.rating,
            "created_at": existing_rating.created_at,
            "updated_at": existing_rating.updated_at,
        }
    else:
        # Создаем новый рейтинг
        new_rating = UserFilmRating(
            user_id=user.id,
            film_id=film_id,
            rating=rating_data.rating
        )
        session.add(new_rating)
        await session.commit()
        await session.refresh(new_rating)
        
        # Обновляем средний рейтинг фильма
        await update_film_user_rating(session, film_id)
        
        return {
            "rating": new_rating.rating,
            "created_at": new_rating.created_at,
            "updated_at": new_rating.updated_at,
        }


@router.put("/films/{film_id}/rating", summary="Изменить рейтинг для фильма")
async def update_user_film_rating(
    film_id: int,
    rating_data: UserFilmRatingUpdate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Изменить рейтинг пользователя для фильма"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Проверяем, что рейтинг существует
    rating_stmt = select(UserFilmRating).where(
        and_(
            UserFilmRating.user_id == user.id,
            UserFilmRating.film_id == film_id
        )
    )
    rating_result = await session.execute(rating_stmt)
    rating = rating_result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=404,
            detail="User rating not found. Use POST to create a new rating."
        )
    
    # Обновляем рейтинг
    rating.rating = rating_data.rating
    await session.commit()
    await session.refresh(rating)
    
    # Обновляем средний рейтинг фильма
    await update_film_user_rating(session, film_id)
    
    return {
        "rating": rating.rating,
        "created_at": rating.created_at,
        "updated_at": rating.updated_at,
    }


@router.delete("/films/{film_id}/rating", summary="Удалить рейтинг для фильма")
async def delete_user_film_rating(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить рейтинг пользователя для фильма"""
    rating_stmt = select(UserFilmRating).where(
        and_(
            UserFilmRating.user_id == user.id,
            UserFilmRating.film_id == film_id
        )
    )
    rating_result = await session.execute(rating_stmt)
    rating = rating_result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    await session.delete(rating)
    await session.commit()
    
    # Обновляем средний рейтинг фильма
    await update_film_user_rating(session, film_id)
    
    return {"message": "Rating deleted successfully"}


@router.get("/films/{film_id}/rating/average", response_model=FilmAverageRatingRead, summary="Средний рейтинг фильма")
async def get_film_average_rating(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить средний рейтинг фильма от всех пользователей"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Получаем статистику рейтингов
    stats_stmt = select(
        func.avg(UserFilmRating.rating),
        func.count(UserFilmRating.id),
        func.min(UserFilmRating.rating),
        func.max(UserFilmRating.rating)
    ).where(UserFilmRating.film_id == film_id)
    
    result = await session.execute(stats_stmt)
    avg_rating, total_ratings, min_rating, max_rating = result.first()
    
    if total_ratings and total_ratings > 0:
        return FilmAverageRatingRead(
            average_rating=round(float(avg_rating), 2) if avg_rating else None,
            total_ratings=total_ratings,
            min_rating=float(min_rating) if min_rating else None,
            max_rating=float(max_rating) if max_rating else None,
        )
    else:
        return FilmAverageRatingRead(
            average_rating=None,
            total_ratings=0,
            min_rating=None,
            max_rating=None,
        )


@router.get("/users/{user_id}/ratings", response_model=UserRatingsResponse, summary="Рейтинги пользователя")
async def get_user_ratings(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить все рейтинги указанного пользователя"""
    # Проверяем, что пользователь существует
    user_stmt = select(User).where(User.id == user_id)
    user_result = await session.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    offset = (page - 1) * page_size
    
    # Получаем общее количество рейтингов пользователя
    total_count_stmt = select(func.count(UserFilmRating.id)).where(UserFilmRating.user_id == user_id)
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем рейтинги с информацией о фильмах
    ratings_stmt = (
        select(UserFilmRating)
        .options(selectinload(UserFilmRating.film))
        .where(UserFilmRating.user_id == user_id)
        .order_by(UserFilmRating.updated_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    ratings_result = await session.execute(ratings_stmt)
    ratings = ratings_result.scalars().all()
    
    items = []
    for rating in ratings:
        # Правильно создаем объект FilmRead с помощью Pydantic
        film_data = FilmRead.model_validate(rating.film) if rating.film else None

        items.append(UserFilmRatingRead(
            id=rating.id,
            user_id=rating.user_id,
            film_id=rating.film_id,
            rating=rating.rating,
            created_at=rating.created_at,
            updated_at=rating.updated_at,
            film=film_data
        ))
    
    return UserRatingsResponse(
        items=items,
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )
