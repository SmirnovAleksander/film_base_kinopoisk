from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from core.config import settings
from core.models import db_helper, Comment, Film, User
from core.schemas import (
    CommentCreate,
    CommentUpdate,
    CommentRead,
    CommentModerationRead,
    CommentModerationResponse,
    CommentModerationStats,
)
from api.api_v1.fastapi_users import current_active_user, current_active_superuser

router = APIRouter(
    prefix=settings.api.v1.prefix + "/comments",
    tags=["Comments"],
)


@router.get("/{film_id}", response_model=List[CommentRead], summary="Список комментариев к фильму")
async def list_comments(
    film_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список комментариев к фильму"""
    stmt = (
        select(Comment)
        .where(
            and_(
                Comment.film_id == film_id,
                Comment.is_deleted == False,
                Comment.status == "approved"
            )
        )
        .order_by(Comment.created_at.desc())
    )
    result = await session.execute(stmt)
    comments = result.scalars().all()
    
    return [CommentRead.model_validate(comment) for comment in comments]


@router.post("/{film_id}", summary="Добавить комментарий")
async def add_comment(
    film_id: int,
    comment_data: CommentCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Добавить комментарий к фильму"""
    # Проверяем, что фильм существует
    film_stmt = select(Film).where(Film.id == film_id)
    film_result = await session.execute(film_stmt)
    film = film_result.scalar_one_or_none()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Создаем комментарий
    comment = Comment(
        user_id=user.id,
        film_id=film_id,
        content=comment_data.content,
        status="pending"  # Комментарии требуют модерации
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    return {"id": comment.id, "status": "pending_moderation"}


@router.put("/{comment_id}", summary="Редактировать комментарий")
async def edit_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Редактировать комментарий"""
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.is_deleted:
        raise HTTPException(status_code=400, detail="Comment is deleted")
    
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Обновляем комментарий
    comment.content = comment_data.content
    comment.is_edited = True
    comment.status = "pending"  # Отредактированные комментарии требуют повторной модерации
    
    await session.commit()
    
    return {"status": "updated", "requires_moderation": True}


@router.delete("/{comment_id}", summary="Удалить комментарий")
async def delete_comment(
    comment_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить комментарий (мягкое удаление)"""
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Мягкое удаление
    comment.is_deleted = True
    await session.commit()
    
    return {"status": "deleted"}


# Эндпоинты для модерации (только для суперпользователей)

@router.get("/moderation/pending", response_model=CommentModerationResponse, summary="Комментарии на модерации")
async def get_pending_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(current_active_superuser),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить комментарии, ожидающие модерации (только для суперпользователей)"""
    offset = (page - 1) * page_size
    
    # Получаем комментарии с информацией о фильме и пользователе
    stmt = (
        select(Comment)
        .options(
            selectinload(Comment.film),
            selectinload(Comment.user)
        )
        .where(Comment.status == "pending")
        .order_by(Comment.created_at.asc())
        .offset(offset)
        .limit(page_size)
    )
    result = await session.execute(stmt)
    comments = result.scalars().all()
    
    # Получаем общее количество
    count_stmt = select(func.count(Comment.id)).where(Comment.status == "pending")
    count_result = await session.execute(count_stmt)
    total_count = count_result.scalar()
    
    items = []
    for comment in comments:
        items.append({
            "id": comment.id,
            "user_id": comment.user_id,
            "film_id": comment.film_id,
            "content": comment.content,
            "is_edited": comment.is_edited,
            "is_deleted": comment.is_deleted,
            "status": comment.status,
            "created_at": comment.created_at,
            "edited_at": comment.edited_at,
            "moderated_at": comment.moderated_at,
            "film_title": comment.film.title if comment.film else None,
            "user_email": comment.user.email if comment.user else None,
            "username": getattr(comment.user, 'username', None) if comment.user else None,
        })
    
    return CommentModerationResponse(
        items=items,
        page=page,
        page_size=page_size,
        total_count=total_count or 0,
        total_pages=(total_count + page_size - 1) // page_size if total_count else 0,
    )


@router.put("/{comment_id}/moderate", summary="Модерировать комментарий")
async def moderate_comment(
    comment_id: int,
    action: str = Query(..., description="Действие: approve, reject, delete"),
    user: User = Depends(current_active_superuser),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Модерировать комментарий (только для суперпользователей)"""
    if action not in ["approve", "reject", "delete"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid action. Must be: approve, reject, or delete"
        )
    
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Применяем действие модерации
    if action == "approve":
        comment.status = "approved"
    elif action == "reject":
        comment.status = "rejected"
    elif action == "delete":
        comment.is_deleted = True
        comment.status = "deleted"
    
    await session.commit()
    
    return {"message": f"Comment {action}d successfully"}


@router.get("/moderation/stats", response_model=CommentModerationStats, summary="Статистика модерации")
async def get_moderation_stats(
    user: User = Depends(current_active_superuser),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить статистику модерации комментариев (только для суперпользователей)"""
    # Общее количество комментариев
    total_stmt = select(func.count(Comment.id))
    total_result = await session.execute(total_stmt)
    total_comments = total_result.scalar()
    
    # Статистика по статусам
    status_stmt = select(Comment.status, func.count(Comment.id)).group_by(Comment.status)
    status_result = await session.execute(status_stmt)
    status_stats = {row[0]: row[1] for row in status_result.all()}
    
    # Комментарии за последние 7 дней
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    comments_7d_stmt = select(func.count(Comment.id)).where(Comment.created_at >= seven_days_ago)
    comments_7d_result = await session.execute(comments_7d_stmt)
    comments_7d = comments_7d_result.scalar()
    
    # Комментарии на модерации
    pending_stmt = select(func.count(Comment.id)).where(Comment.status == "pending")
    pending_result = await session.execute(pending_stmt)
    pending_comments = pending_result.scalar()
    
    return CommentModerationStats(
        total_comments=total_comments or 0,
        status_distribution=status_stats,
        comments_7d=comments_7d or 0,
        pending_comments=pending_comments or 0,
    )
