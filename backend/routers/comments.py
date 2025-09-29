from typing import List

from fastapi import APIRouter, Depends, HTTPException

from ..utils.db import get_conn
from ..utils.auth import get_current_user_id


router = APIRouter()


@router.get("/{film_id}")
def list_comments(film_id: int, conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, user_id, content, rating, is_edited, is_deleted, status, created_at FROM comments WHERE film_id=%s AND is_deleted=FALSE ORDER BY created_at DESC", (film_id,))
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "user_id": r[1],
                "content": r[2],
                "rating": r[3],
                "is_edited": r[4],
                "is_deleted": r[5],
                "status": r[6],
                "created_at": r[7].isoformat() if r[7] else None,
            } for r in rows
        ]
    finally:
        cur.close()


@router.post("/{film_id}")
def add_comment(film_id: int, content: str, rating: int | None = None, user_id: int = Depends(get_current_user_id), conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        if rating is not None and (rating < 1 or rating > 10):
            raise HTTPException(status_code=400, detail="Rating must be 1..10")
        cur.execute("INSERT INTO comments (film_id, user_id, content, rating) VALUES (%s, %s, %s, %s) RETURNING id",
                    (film_id, user_id, content, rating))
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"id": new_id}
    finally:
        cur.close()


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, user_id: int = Depends(get_current_user_id), conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM comments WHERE id=%s", (comment_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Comment not found")
        if row[0] != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        cur.execute("UPDATE comments SET is_deleted=TRUE WHERE id=%s", (comment_id,))
        conn.commit()
        return {"status": "deleted"}
    finally:
        cur.close()


