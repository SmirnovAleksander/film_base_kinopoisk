from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import db_helper, UserFilmHistory, Film, User, Genre
from core.schemas import UserFilmHistoryResponse, UserFilmHistoryStats, FilmRead, UserFilmHistoryRead
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.post("/films/{film_id}/visit", summary="Добавить фильм в историю")
async def add_film_to_history(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Добавить фильм в историю посещений пользователя"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    # Проверяем, есть ли уже запись в истории
    existing_stmt = select(UserFilmHistory).where(
        and_(
            UserFilmHistory.user_id == user.id,
            UserFilmHistory.film_id == film_id
        )
    )
    existing_result = await session.execute(existing_stmt)
    existing_history = existing_result.scalar_one_or_none()
    
    if existing_history:
        # Обновляем время посещения
        from datetime import datetime
        existing_history.visited_at = datetime.utcnow()
    else:
        # Создаем новую запись
        history = UserFilmHistory(user_id=user.id, film_id=film_id)
        session.add(history)
    
    await session.commit()
    
    # Удаляем старые записи, оставляя только последние 10
    # Получаем все записи пользователя, отсортированные по времени
    all_history_stmt = (
        select(UserFilmHistory)
        .where(UserFilmHistory.user_id == user.id)
        .order_by(desc(UserFilmHistory.visited_at))
    )
    all_history_result = await session.execute(all_history_stmt)
    all_history = all_history_result.scalars().all()
    
    # Удаляем записи после 10-й
    if len(all_history) > 10:
        for old_record in all_history[10:]:
            await session.delete(old_record)
        await session.commit()
    
    return {"message": "Фильм добавлен в историю посещений"}


@router.get("/films", response_model=UserFilmHistoryResponse, summary="История посещений")
async def get_user_film_history(
    limit: int = Query(10, ge=1, le=50, description="Количество записей"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить историю посещений фильмов пользователя"""
    stmt = (
        select(UserFilmHistory)
        .options(selectinload(UserFilmHistory.film))
        .where(UserFilmHistory.user_id == user.id)
        .order_by(desc(UserFilmHistory.visited_at))
        .limit(limit)
    )
    result = await session.execute(stmt)
    history_records = result.scalars().all()
    
    history = []
    for record in history_records:
        if record.film:
            # Правильно создаем объект FilmRead с помощью Pydantic
            film_data = FilmRead.model_validate(record.film)

            history.append(UserFilmHistoryRead(
                visited_at=record.visited_at,
                film=film_data
            ))

    return UserFilmHistoryResponse(
        history=history,
        total=len(history)
    )


@router.delete("/films", summary="Очистить историю")
async def clear_user_film_history(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Очистить всю историю посещений пользователя"""
    # Получаем все записи истории пользователя
    stmt = select(UserFilmHistory).where(UserFilmHistory.user_id == user.id)
    result = await session.execute(stmt)
    history_records = result.scalars().all()
    
    # Удаляем все записи
    for record in history_records:
        await session.delete(record)
    
    await session.commit()
    
    return {"message": "История посещений очищена"}


@router.delete("/films/{film_id}", summary="Удалить фильм из истории")
async def remove_film_from_history(
    film_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить конкретный фильм из истории посещений пользователя"""
    stmt = select(UserFilmHistory).where(
        and_(
            UserFilmHistory.user_id == user.id,
            UserFilmHistory.film_id == film_id
        )
    )
    result = await session.execute(stmt)
    history_record = result.scalar_one_or_none()
    
    if not history_record:
        raise HTTPException(status_code=404, detail="Фильм не найден в истории")
    
    await session.delete(history_record)
    await session.commit()
    
    return {"message": "Фильм удален из истории посещений"}


@router.get("/films/stats", response_model=UserFilmHistoryStats, summary="Статистика истории")
async def get_history_stats(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить статистику истории посещений пользователя"""
    # Общее количество посещений
    total_stmt = select(func.count(UserFilmHistory.id)).where(
        UserFilmHistory.user_id == user.id
    )
    total_result = await session.execute(total_stmt)
    total_visits = total_result.scalar()
    
    # Посещения за последние 7 дней
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    visits_7d_stmt = select(func.count(UserFilmHistory.id)).where(
        and_(
            UserFilmHistory.user_id == user.id,
            UserFilmHistory.visited_at >= seven_days_ago
        )
    )
    visits_7d_result = await session.execute(visits_7d_stmt)
    visits_7d = visits_7d_result.scalar()
    
    # Посещения за последние 30 дней
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    visits_30d_stmt = select(func.count(UserFilmHistory.id)).where(
        and_(
            UserFilmHistory.user_id == user.id,
            UserFilmHistory.visited_at >= thirty_days_ago
        )
    )
    visits_30d_result = await session.execute(visits_30d_stmt)
    visits_30d = visits_30d_result.scalar()
    
    # Самый популярный жанр в истории
    # Это сложный запрос, который требует JOIN через несколько таблиц
    favorite_genre_stmt = (
        select(Genre.name, func.count(Genre.id).label('count'))
        .select_from(UserFilmHistory)
        .join(Film, UserFilmHistory.film_id == Film.id)
        .join(Film.genres)
        .where(UserFilmHistory.user_id == user.id)
        .group_by(Genre.name)
        .order_by(desc('count'))
        .limit(1)
    )
    favorite_genre_result = await session.execute(favorite_genre_stmt)
    favorite_genre_row = favorite_genre_result.first()
    
    favorite_genre = favorite_genre_row[0] if favorite_genre_row else None
    favorite_genre_count = favorite_genre_row[1] if favorite_genre_row else 0
    
    return UserFilmHistoryStats(
        total_visits=total_visits or 0,
        visits_7d=visits_7d or 0,
        visits_30d=visits_30d or 0,
        favorite_genre=favorite_genre,
        favorite_genre_count=favorite_genre_count,
    )
