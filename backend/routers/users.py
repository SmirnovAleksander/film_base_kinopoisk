from fastapi import APIRouter, Depends, HTTPException

from ..utils.auth import get_current_user_id
from ..utils.db import get_conn


router = APIRouter()


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user_id), conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, email, username, is_email_verified, role, created_at, last_login_at FROM users WHERE id=%s", (user_id,))
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


