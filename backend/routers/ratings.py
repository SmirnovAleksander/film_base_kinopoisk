from fastapi import APIRouter, Depends, HTTPException

from ..utils.db import get_conn
from ..utils.auth import get_current_user_id


router = APIRouter()


@router.post("/{film_id}")
def upsert_rating(film_id: int, score: int, user_id: int = Depends(get_current_user_id), conn = Depends(get_conn)):
    if score < 1 or score > 10:
        raise HTTPException(status_code=400, detail="Score must be 1..10")
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO film_ratings (film_id, user_id, score)
            VALUES (%s, %s, %s)
            ON CONFLICT (film_id, user_id) DO UPDATE SET score=EXCLUDED.score, updated_at=NOW()
            """,
            (film_id, user_id, score)
        )
        conn.commit()
        return {"status": "ok"}
    finally:
        cur.close()


@router.get("/{film_id}")
def get_rating_aggregate(film_id: int, conn = Depends(get_conn)):
    cur = conn.cursor()
    try:
        cur.execute("SELECT AVG(score), COUNT(*) FROM film_ratings WHERE film_id=%s", (film_id,))
        r = cur.fetchone()
        avg = float(r[0]) if r and r[0] is not None else None
        count = int(r[1]) if r and r[1] is not None else 0
        return {"avg": avg, "count": count}
    finally:
        cur.close()


