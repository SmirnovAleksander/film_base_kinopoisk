from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..utils.db import get_connection


router = APIRouter()


@router.get("/", summary="Список фильмов")
def list_films(page: int = 1, page_size: int = 20):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    offset = (page - 1) * page_size
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, kinopoisk_id, title, poster, rating_kp FROM films ORDER BY id LIMIT %s OFFSET %s", (page_size, offset))
            rows = cur.fetchall()
            films = []
            for r in rows:
                films.append({
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "title": r[2],
                    "poster": r[3],
                    "rating_kp": r[4],
                })
            return {"items": films, "page": page, "page_size": page_size}
        finally:
            cur.close()


@router.get("/countries", summary="Все страны (справочник)")
def list_countries():
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name FROM countries ORDER BY name")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1]} for r in rows]
        finally:
            cur.close()


@router.get("/genres", summary="Все жанры (справочник)")
def list_genres():
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name FROM genres ORDER BY name")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1]} for r in rows]
        finally:
            cur.close()

@router.get("/filter", summary="Фильмы по фильтрам: жанр/страна/год или диапазон лет")
def films_filter(
    genre_id: Optional[int] = Query(None, description="ID жанра"),
    country_id: Optional[int] = Query(None, description="ID страны"),
    year: Optional[int] = Query(None, description="Конкретный год выпуска"),
    start_year: Optional[int] = Query(None, description="Начальный год (включительно)"),
    end_year: Optional[int] = Query(None, description="Конечный год (включительно)"),
    source: str = Query("kp", description="Источник рейтинга: 'kp' или 'imdb'"),
    min_rating: Optional[float] = Query(None, description="Минимальный рейтинг включительно"),
    max_rating: Optional[float] = Query(None, description="Максимальный рейтинг включительно"),
    page: int = 1,
    page_size: int = 20,
):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    if source not in ("kp", "imdb"):
        raise HTTPException(status_code=400, detail="source must be 'kp' or 'imdb'")

    # Если задан конкретный год, игнорируем диапазон (поведение как в /by-year)
    use_range = year is None

    offset = (page - 1) * page_size

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            joins = []
            conditions = []
            params: list = []

            if genre_id is not None:
                joins.append("JOIN film_genres fg ON fg.film_id = f.id")
                conditions.append("fg.genre_id = %s")
                params.append(genre_id)

            if country_id is not None:
                joins.append("JOIN film_countries fc ON fc.film_id = f.id")
                conditions.append("fc.country_id = %s")
                params.append(country_id)

            if year is not None:
                conditions.append("f.year = %s")
                params.append(year)
            elif use_range and (start_year is not None or end_year is not None):
                if start_year is not None:
                    conditions.append("f.year >= %s")
                    params.append(start_year)
                if end_year is not None:
                    conditions.append("f.year <= %s")
                    params.append(end_year)

            # Фильтр по рейтингу (опционально)
            rating_column = "rating_kp" if source == "kp" else "rating_imdb"
            if min_rating is not None:
                conditions.append(f"CAST(f.{rating_column} AS NUMERIC) >= %s")
                params.append(min_rating)
            if max_rating is not None:
                conditions.append(f"CAST(f.{rating_column} AS NUMERIC) <= %s")
                params.append(max_rating)

            joins_sql = "\n".join(joins)
            where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

            sql = f"""
                SELECT f.id, f.kinopoisk_id, f.title, f.poster, f.rating_kp
                FROM films f
                {joins_sql}
                {where_clause}
                ORDER BY f.id
                LIMIT %s OFFSET %s
            """
            params.extend([page_size, offset])
            cur.execute(sql, tuple(params))

            rows = cur.fetchall()
            items = [
                {
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "title": r[2],
                    "poster": r[3],
                    "rating_kp": r[4],
                }
                for r in rows
            ]
            return {"items": items, "page": page, "page_size": page_size}
        finally:
            cur.close()

@router.get("/{film_id}", summary="Детали фильма")
def get_film(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, kinopoisk_id, title, original_title, description, full_description, poster, year, duration, rating_kp, kp_votes_count, rating_imdb, imdb_votes_count FROM films WHERE id=%s", (film_id,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Film not found")
            return {
                "id": r[0],
                "kinopoisk_id": r[1],
                "title": r[2],
                "original_title": r[3],
                "description": r[4],
                "full_description": r[5],
                "poster": r[6],
                "year": r[7],
                "duration": r[8],
                "rating_kp": r[9],
                "kp_votes_count": r[10],
                "rating_imdb": r[11],
                "imdb_votes_count": r[12],
            }
        finally:
            cur.close()


@router.get("/{film_id}/similar", summary="Похожие фильмы")
def get_similar_films(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT similar_film_id, similar_film_title FROM similar_films WHERE film_id=%s", (film_id,))
            rows = cur.fetchall()
            return [{"kinopoisk_id": r[0], "title": r[1]} for r in rows]
        finally:
            cur.close()


@router.get("/{film_id}/persons", summary="Список персон, участвовавших в фильме")
def get_film_persons(film_id: int, role: str = Query("all", description="Роль персоны (например: actor, director, writer). 'all' — без фильтра")):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            if role and role.lower() != "all":
                cur.execute(
                    """
                    SELECT p.id, p.kinopoisk_id, p.name, p.english_name, p.photo, fp.role
                    FROM film_person fp
                    JOIN person p ON p.id = fp.person_id
                    WHERE fp.film_id = %s AND fp.role = %s
                    ORDER BY p.id
                    """,
                    (film_id, role)
                )
            else:
                cur.execute(
                    """
                    SELECT p.id, p.kinopoisk_id, p.name, p.english_name, p.photo, fp.role
                    FROM film_person fp
                    JOIN person p ON p.id = fp.person_id
                    WHERE fp.film_id = %s
                    ORDER BY p.id
                    """,
                    (film_id,)
                )
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "name": r[2],
                    "english_name": r[3],
                    "photo": r[4],
                    "role": r[5],
                }
                for r in rows
            ]
        finally:
            cur.close()
