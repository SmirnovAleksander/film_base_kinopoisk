from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..utils.db import get_connection
from ..utils.auth import get_current_user_id


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


