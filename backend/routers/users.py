from fastapi import APIRouter, Depends, HTTPException

from ..utils.auth import get_current_user_id
from ..utils.db import get_connection


router = APIRouter()


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user_id)):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, email, username, is_email_verified, role, created_at, last_login_at FROM app_user WHERE id=%s", (user_id,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="User not found")
            return {
                "id": r[0],
                "email": r[1],
                "username": r[2],
                "is_email_verified": r[3],
                "role": r[4],
                "created_at": r[5].isoformat() if r[5] else None,
                "last_login_at": r[6].isoformat() if r[6] else None,
            }
        finally:
            cur.close()


@router.get("/count", summary="Количество всех пользователей")
def get_users_count():
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM app_user")
            count = cur.fetchone()[0]
            return {"count": count}
        finally:
            cur.close()

