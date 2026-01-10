from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from core.models import ( 
    db_helper, 
    UserContentRating, 
    Film, 
    Series,
    User
)
from core.schemas.film import FilmRead, SeriesRead
from core.schemas.user_interactions import (
    UserContentRatingCreate,
    UserContentRatingUpdate,
    UserContentRatingRead,
    ContentAverageRatingRead,
    UserRatingsResponse,
)
from core.schemas.base import (
    RatingOperationResponse,
    MessageResponse,
)
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)


async def update_content_user_rating(session: AsyncSession, content_id: int, content_type: str):
    """Обновляет средний пользовательский рейтинг контента"""
    # Вычисляем средний рейтинг и количество оценок
    avg_stmt = select(
        func.avg(UserContentRating.rating),
        func.count(UserContentRating.id)
    ).where(
        and_(
            UserContentRating.content_id == content_id,
            UserContentRating.content_type == content_type
        )
    )
    
    result = await session.execute(avg_stmt)
    avg_rating, rating_count = result.first()
    
    # Обновляем таблицу film или series
    if content_type == "film":
        stmt = select(Film).where(Film.id == content_id)
    else:
        stmt = select(Series).where(Series.id == content_id)
        
    res = await session.execute(stmt)
    content = res.scalar_one_or_none()
    
    if content:
        content.user_rating = avg_rating
        content.user_rating_count = rating_count or 0
        await session.commit()


# GET /api/v1/ratings/film/1 - Получить оценку, которую текущий пользователь поставил контенту
@router.get("/{content_type}/{content_id}", response_model=RatingOperationResponse, summary="Получить рейтинг пользователя")
async def get_user_content_rating(
    content_type: str,
    content_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить рейтинг текущего пользователя для фильма или сериала"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    # Проверяем существование контента
    if content_type == "film":
        stmt = select(Film).where(Film.id == content_id)
    else:
        stmt = select(Series).where(Series.id == content_id)
        
    result = await session.execute(stmt)
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail=f"{content_type.capitalize()} not found")
    
    # Получаем рейтинг пользователя
    rating_stmt = select(UserContentRating).where(
        and_(
            UserContentRating.user_id == user.id,
            UserContentRating.content_id == content_id,
            UserContentRating.content_type == content_type
        )
    )
    rating_result = await session.execute(rating_stmt)
    rating = rating_result.scalar_one_or_none()
    
    if rating:
        return RatingOperationResponse(
            rating=rating.rating,
            created_at=rating.created_at,
            updated_at=rating.updated_at,
        )
    else:
        return RatingOperationResponse(rating=None, created_at=None, updated_at=None)


# POST /api/v1/ratings/series/1 - Поставить новую оценку или изменить существующую (от 1 до 10)
@router.post("/{content_type}/{content_id}", response_model=RatingOperationResponse, summary="Установить рейтинг")
async def set_user_content_rating(
    content_type: str,
    content_id: int,
    rating_data: UserContentRatingCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Установить или обновить рейтинг пользователя для контента"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    # Проверяем существование контента
    if content_type == "film":
        stmt = select(Film).where(Film.id == content_id)
    else:
        stmt = select(Series).where(Series.id == content_id)
        
    result = await session.execute(stmt)
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail=f"{content_type.capitalize()} not found")
    
    # Проверяем, есть ли уже рейтинг
    existing_stmt = select(UserContentRating).where(
        and_(
            UserContentRating.user_id == user.id,
            UserContentRating.content_id == content_id,
            UserContentRating.content_type == content_type
        )
    )
    existing_result = await session.execute(existing_stmt)
    existing_rating = existing_result.scalar_one_or_none()
    
    if existing_rating:
        # Обновляем существующий рейтинг
        existing_rating.rating = rating_data.rating
        await session.commit()
        await session.refresh(existing_rating)
        
        # Обновляем средний рейтинг контента
        await update_content_user_rating(session, content_id, content_type)
        
        return RatingOperationResponse(
            rating=existing_rating.rating,
            created_at=existing_rating.created_at,
            updated_at=existing_rating.updated_at,
        )
    else:
        # Создаем новый рейтинг
        new_rating = UserContentRating(
            user_id=user.id,
            content_id=content_id,
            content_type=content_type,
            rating=rating_data.rating
        )
        session.add(new_rating)
        await session.commit()
        await session.refresh(new_rating)
        
        # Обновляем средний рейтинг контента
        await update_content_user_rating(session, content_id, content_type)
        
        return RatingOperationResponse(
            rating=new_rating.rating,
            created_at=new_rating.created_at,
            updated_at=new_rating.updated_at,
        )


# DELETE /api/v1/ratings/film/1 - Удалить свою оценку у конкретного фильма или сериала
@router.delete("/{content_type}/{content_id}", response_model=MessageResponse, summary="Удалить рейтинг")
async def delete_user_content_rating(
    content_type: str,
    content_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить рейтинг пользователя для контента"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    rating_stmt = select(UserContentRating).where(
        and_(
            UserContentRating.user_id == user.id,
            UserContentRating.content_id == content_id,
            UserContentRating.content_type == content_type
        )
    )
    rating_result = await session.execute(rating_stmt)
    rating = rating_result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    await session.delete(rating)
    await session.commit()
    
    # Обновляем средний рейтинг контента
    await update_content_user_rating(session, content_id, content_type)
    
    return MessageResponse(message="Rating deleted successfully")


# GET /api/v1/ratings/series/1/average - Получить общую статистику оценок всех пользователей для этого контента
@router.get("/{content_type}/{content_id}/average", response_model=ContentAverageRatingRead, summary="Средний рейтинг")
async def get_content_average_rating(
    content_type: str,
    content_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить средний рейтинг контента от всех пользователей"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    # Проверяем существование контента
    if content_type == "film":
        stmt = select(Film).where(Film.id == content_id)
    else:
        stmt = select(Series).where(Series.id == content_id)
        
    result = await session.execute(stmt)
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail=f"{content_type.capitalize()} not found")
    
    # Получаем статистику рейтингов
    stats_stmt = select(
        func.avg(UserContentRating.rating),
        func.count(UserContentRating.id),
        func.min(UserContentRating.rating),
        func.max(UserContentRating.rating)
    ).where(
        and_(
            UserContentRating.content_id == content_id,
            UserContentRating.content_type == content_type
        )
    )
    
    result = await session.execute(stats_stmt)
    avg_rating, total_ratings, min_rating, max_rating = result.first()
    
    if total_ratings and total_ratings > 0:
        return ContentAverageRatingRead(
            average_rating=round(float(avg_rating), 2) if avg_rating else None,
            total_ratings=total_ratings,
            min_rating=float(min_rating) if min_rating else None,
            max_rating=float(max_rating) if max_rating else None,
        )
    else:
        return ContentAverageRatingRead(
            average_rating=None,
            total_ratings=0,
            min_rating=None,
            max_rating=None,
        )


# GET /api/v1/ratings/users/1/ratings - Список всех оценок, выставленных конкретным пользователем
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
    total_count_stmt = select(func.count(UserContentRating.id)).where(UserContentRating.user_id == user_id)
    total_count_result = await session.execute(total_count_stmt)
    total_count = total_count_result.scalar()
    
    # Получаем рейтинги с информацией о контенте
    ratings_stmt = (
        select(UserContentRating)
        .options(selectinload(UserContentRating.film), selectinload(UserContentRating.series))
        .where(UserContentRating.user_id == user_id)
        .order_by(UserContentRating.updated_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    ratings_result = await session.execute(ratings_stmt)
    ratings = ratings_result.scalars().all()
    
    items = []
    for rating in ratings:
        film_data = FilmRead.model_validate(rating.film) if rating.content_type == "film" and rating.film else None
        series_data = SeriesRead.model_validate(rating.series) if rating.content_type == "series" and rating.series else None

        items.append(UserContentRatingRead(
            id=rating.id,
            user_id=rating.user_id,
            content_id=rating.content_id,
            content_type=rating.content_type,
            rating=rating.rating,
            created_at=rating.created_at,
            updated_at=rating.updated_at,
            film=film_data,
            series=series_data
        ))
    
    return UserRatingsResponse(
        items=items,
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
    )
