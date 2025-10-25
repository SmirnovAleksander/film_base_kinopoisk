from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from core.config import settings
from core.models import db_helper, Comment, Film, User
from core.schemas import (
    CommentCreate,
    CommentUpdate,
    CommentRead,
)
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/comments",
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
                Comment.is_deleted == False
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
        content=comment_data.content
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    return {"id": comment.id, "status": "created"}


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
    
    await session.commit()
    
    return {"status": "updated"}


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

