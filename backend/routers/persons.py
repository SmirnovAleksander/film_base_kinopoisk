from fastapi import APIRouter, Depends, HTTPException

from ..utils.db import get_connection


router = APIRouter()


@router.get("/")
def list_persons(page: int = 1, page_size: int = 20):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    offset = (page - 1) * page_size
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id, kinopoisk_id, name, english_name, photo FROM person ORDER BY id LIMIT %s OFFSET %s",
                (page_size, offset)
            )
            rows = cur.fetchall()
            persons = []
            for r in rows:
                persons.append({
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "name": r[2],
                    "english_name": r[3],
                    "photo": r[4],
                })
            return {"items": persons, "page": page, "page_size": page_size}
        finally:
            cur.close()


@router.get("/{person_id}")
def get_person(person_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT id, kinopoisk_id, name, english_name, career, ganres, height,
                       birthday_day_month, birthday_year, zodiac, age, birthplace,
                       spouse, children, total_films, career_start_year, career_end_year,
                       career_duration, photo
                FROM person WHERE id=%s
                """,
                (person_id,)
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Person not found")
            return {
                "id": r[0],
                "kinopoisk_id": r[1],
                "name": r[2],
                "english_name": r[3],
                "career": r[4],
                "genres": r[5],
                "height": r[6],
                "birthday_day_month": r[7],
                "birthday_year": r[8],
                "zodiac": r[9],
                "age": r[10],
                "birthplace": r[11],
                "spouse": r[12],
                "children": r[13],
                "total_films": r[14],
                "career_start_year": r[15],
                "career_end_year": r[16],
                "career_duration": r[17],
                "photo": r[18],
            }
        finally:
            cur.close()