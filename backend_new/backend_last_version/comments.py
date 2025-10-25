from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..utils.db import get_connection
from ..utils.auth import get_current_user_id, require_moderator


router = APIRouter()


@router.get("/{film_id}")
def list_comments(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, user_id, content, is_edited, is_deleted, status, created_at FROM comment WHERE film_id=%s AND is_deleted=FALSE ORDER BY created_at DESC", (film_id,))
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "user_id": r[1],
                    "content": r[2],
                    "is_edited": r[3],
                    "is_deleted": r[4],
                    "status": r[5],
                    "created_at": r[6].isoformat() if r[6] else None,
                } for r in rows
            ]
        finally:
            cur.close()


@router.post("/{film_id}")
def add_comment(film_id: int, content: str, user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO comment (film_id, user_id, content) VALUES (%s, %s, %s) RETURNING id",
                        (film_id, user_id, content))
            new_id = cur.fetchone()[0]
            conn.commit()
            return {"id": new_id}
        finally:
            cur.close()


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT user_id FROM comment WHERE id=%s", (comment_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Comment not found")
            if row[0] != user_id:
                raise HTTPException(status_code=403, detail="Forbidden")
            cur.execute("UPDATE comment SET is_deleted=TRUE WHERE id=%s", (comment_id,))
            conn.commit()
            return {"status": "deleted"}
        finally:
            cur.close()



@router.put("/{comment_id}")
def edit_comment(comment_id: int, content: str, user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT user_id, is_deleted FROM comment WHERE id=%s", (comment_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Comment not found")
            if row[1]:
                raise HTTPException(status_code=400, detail="Comment is deleted")
            if row[0] != user_id:
                raise HTTPException(status_code=403, detail="Forbidden")
            cur.execute(
                "UPDATE comment SET content=%s, is_edited=TRUE, edited_at=NOW() WHERE id=%s",
                (content, comment_id),
            )
            conn.commit()
            return {"status": "updated"}
        finally:
            cur.close()


@router.get("/moderation/pending", summary="Комментарии на модерации (только для модераторов)")
def get_pending_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    moderator_role: str = Depends(require_moderator())
):
    """Получает комментарии, ожидающие модерации"""
    offset = (page - 1) * page_size
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT c.id, c.film_id, c.user_id, c.content, c.created_at, 
                       f.title as film_title, u.email as user_email, u.username
                FROM comment c
                JOIN film f ON c.film_id = f.id
                JOIN app_user u ON c.user_id = u.id
                WHERE c.status = 'pending'
                ORDER BY c.created_at ASC
                LIMIT %s OFFSET %s
                """,
                (page_size, offset)
            )
            
            rows = cur.fetchall()
            comments = []
            for r in rows:
                comments.append({
                    "id": r[0],
                    "film_id": r[1],
                    "user_id": r[2],
                    "content": r[3],
                    "created_at": r[4].isoformat() if r[4] else None,
                    "film_title": r[5],
                    "user_email": r[6],
                    "username": r[7]
                })
            
            # Получаем общее количество
            cur.execute("SELECT COUNT(*) FROM comment WHERE status = 'pending'")
            total_count = cur.fetchone()[0]
            
            return {
                "items": comments,
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size
            }
        finally:
            cur.close()


@router.put("/{comment_id}/moderate", summary="Модерировать комментарий (только для модераторов)")
def moderate_comment(
    comment_id: int,
    action: str,  # "approve", "reject", "delete"
    moderator_role: str = Depends(require_moderator())
):
    """Модерирует комментарий (одобрить/отклонить/удалить)"""
    if action not in ["approve", "reject", "delete"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be: approve, reject, or delete")
    
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Проверяем, что комментарий существует
            cur.execute("SELECT id, status FROM comment WHERE id = %s", (comment_id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Comment not found")
            
            if action == "approve":
                cur.execute(
                    "UPDATE comment SET status = 'approved', moderated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (comment_id,)
                )
            elif action == "reject":
                cur.execute(
                    "UPDATE comment SET status = 'rejected', moderated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (comment_id,)
                )
            elif action == "delete":
                cur.execute(
                    "UPDATE comment SET is_deleted = TRUE, status = 'deleted', moderated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (comment_id,)
                )
            
            conn.commit()
            return {"message": f"Comment {action}d successfully"}
        finally:
            cur.close()


@router.get("/moderation/stats", summary="Статистика модерации (только для модераторов)")
def get_moderation_stats(moderator_role: str = Depends(require_moderator())):
    """Получает статистику модерации комментариев"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Общая статистика комментариев
            cur.execute("SELECT COUNT(*) FROM comment")
            total_comments = cur.fetchone()[0]
            
            # Статистика по статусам
            cur.execute("SELECT status, COUNT(*) FROM comment GROUP BY status")
            status_stats = {row[0]: row[1] for row in cur.fetchall()}
            
            # Комментарии за последние 7 дней
            cur.execute(
                "SELECT COUNT(*) FROM comment WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'"
            )
            comments_7d = cur.fetchone()[0]
            
            # Комментарии на модерации
            cur.execute("SELECT COUNT(*) FROM comment WHERE status = 'pending'")
            pending_comments = cur.fetchone()[0]
            
            return {
                "total_comments": total_comments,
                "status_distribution": status_stats,
                "comments_7d": comments_7d,
                "pending_comments": pending_comments
            }
        finally:
            cur.close()


