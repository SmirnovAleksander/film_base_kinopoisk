from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from core.models import ( 
    db_helper, 
    Comment, 
    Film, 
    Series,
    User 
)
from core.schemas.user_interactions import (
    CommentCreate,
    CommentUpdate,
    CommentRead,
)
from core.schemas.base import CommentOperationResponse
from api.api_v1.fastapi_users import current_active_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


# GET /api/v1/comments/film/1 - Получить все публичные комментарии к фильму или сериалу
@router.get("/{content_type}/{content_id}", response_model=List[CommentRead], summary="Список комментариев")
async def list_comments(
    content_type: str,
    content_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить список комментариев к фильму или сериалу"""
    if content_type not in ("film", "series"):
        raise HTTPException(status_code=400, detail="Invalid content type")

    stmt = (
        select(Comment)
        .where(
            and_(
                Comment.content_id == content_id,
                Comment.content_type == content_type,
                Comment.is_deleted == False
            )
        )
        .order_by(Comment.created_at.desc())
    )
    result = await session.execute(stmt)
    comments = result.scalars().all()
    
    return [CommentRead.model_validate(comment) for comment in comments]


# POST /api/v1/comments/series/1 - Опубликовать новый комментарий от имени текущего пользователя
@router.post("/{content_type}/{content_id}", response_model=CommentOperationResponse, summary="Добавить комментарий")
async def add_comment(
    content_type: str,
    content_id: int,
    comment_data: CommentCreate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Добавить комментарий к фильму или сериалу"""
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
    
    # Создаем комментарий
    comment = Comment(
        user_id=user.id,
        content_id=content_id,
        content_type=content_type,
        content=comment_data.content
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    return CommentOperationResponse(status="created", id=comment.id)


# PUT /api/v1/comments/1 - Изменить текст своего комментария по его ID
@router.put("/{comment_id}", response_model=CommentOperationResponse, summary="Редактировать комментарий")
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
    
    return CommentOperationResponse(status="updated")


# DELETE /api/v1/comments/1 - Пометить свой комментарий как удаленный (мягкое удаление)
@router.delete("/{comment_id}", response_model=CommentOperationResponse, summary="Удалить комментарий")
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
    
    return CommentOperationResponse(status="deleted")

