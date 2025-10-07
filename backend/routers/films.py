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
            # 1) total
            cur.execute("SELECT COUNT(*) FROM film")
            total_count = cur.fetchone()[0] or 0

            # 2) page items
            cur.execute(
                """
                SELECT id,
                       kinopoisk_id,
                       title,
                       original_title,
                       full_description,
                       poster,
                       year,
                       duration,
                       rating_kp,
                       rating_imdb
                FROM film
                ORDER BY id
                LIMIT %s OFFSET %s
                """,
                (page_size, offset)
            )
            rows = cur.fetchall()
            films = []
            for r in rows:
                films.append({
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "title": r[2],
                    "original_title": r[3],
                    "full_description": r[4],
                    "poster": r[5],
                    "year": r[6],
                    "duration": r[7],
                    "rating_kp": r[8],
                    "rating_imdb": r[9],
                })
            return {"items": films, "page": page, "page_size": page_size, "total_count": total_count}
        finally:
            cur.close()



@router.get("/search", summary="Поиск фильмов по названию (ru|en)")
def search_films(
    query: str = Query(..., min_length=1, description="Строка поиска"),
    lang: str = Query("ru", description="Язык названия: 'ru' (title) или 'en' (original_title)"),
    page: int = 1,
    page_size: int = 20,
):
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")

    column = "title" if lang == "ru" else "original_title"
    offset = (page - 1) * page_size
    pattern = f"%{query}%"

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # 1) count matching rows
            count_sql = f"SELECT COUNT(*) FROM film WHERE {column} ILIKE %s"
            cur.execute(count_sql, (pattern,))
            total_count = cur.fetchone()[0] or 0

            # 2) select page
            sql = f"""
                SELECT id,
                       kinopoisk_id,
                       title,
                       original_title,
                       full_description,
                       poster,
                       year,
                       duration,
                       rating_kp,
                       rating_imdb
                FROM film
                WHERE {column} ILIKE %s
                ORDER BY id
                LIMIT %s OFFSET %s
            """
            cur.execute(sql, (pattern, page_size, offset))
            rows = cur.fetchall()
            items = [
                {
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "title": r[2],
                    "original_title": r[3],
                    "full_description": r[4],
                    "poster": r[5],
                    "year": r[6],
                    "duration": r[7],
                    "rating_kp": r[8],
                    "rating_imdb": r[9],
                }
                for r in rows
            ]
            return {"items": items, "page": page, "page_size": page_size, "total_count": total_count}
        finally:
            cur.close()


@router.get("/countries", summary="Все страны (справочник)")
def list_countries():
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name FROM country ORDER BY name")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1]} for r in rows]
        finally:
            cur.close()


@router.get("/genres", summary="Все жанры (справочник)")
def list_genres():
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, name FROM genre ORDER BY name")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1]} for r in rows]
        finally:
            cur.close()

@router.get("/filter", summary="Фильмы по фильтрам: жанр/страна/год или диапазон лет")
def films_filter(
    genre_id: Optional[int] = Query(None, description="ID жанра"),
    country_id: Optional[int] = Query(None, description="ID страны"),
    start_year: Optional[int] = Query(None, description="Начальный год (или конкретный год, если end_year не задан)"),
    end_year: Optional[int] = Query(None, description="Конечный год (включительно)"),
    title: Optional[str] = Query(None, min_length=1, description="Поисковая строка по названию"),
    lang: str = Query("ru", description="Язык названия для поиска: 'ru' (title) или 'en' (original_title)"),
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
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'ru' or 'en'")

    effective_year = start_year
    offset = (page - 1) * page_size

    with get_connection() as conn:
        cur = conn.cursor()
        try:
            joins = []
            conditions = []
            params: list = []

            if genre_id is not None:
                joins.append("JOIN film_genre fg ON fg.film_id = f.id")
                conditions.append("fg.genre_id = %s")
                params.append(genre_id)

            if country_id is not None:
                joins.append("JOIN film_country fc ON fc.film_id = f.id")
                conditions.append("fc.country_id = %s")
                params.append(country_id)

            if effective_year is not None and end_year is None:
                conditions.append("f.year = %s")
                params.append(effective_year)
            elif end_year is not None:
                if effective_year is not None:
                    conditions.append("f.year >= %s")
                    params.append(effective_year)
                conditions.append("f.year <= %s")
                params.append(end_year)

            if title is not None and title.strip() != "":
                column = "f.title" if lang == "ru" else "f.original_title"
                conditions.append(f"{column} ILIKE %s")
                params.append(f"%{title}%")

            rating_column = "rating_kp" if source == "kp" else "rating_imdb"
            if min_rating is not None:
                conditions.append(f"CAST(f.{rating_column} AS NUMERIC) >= %s")
                params.append(min_rating)
            if max_rating is not None:
                conditions.append(f"CAST(f.{rating_column} AS NUMERIC) <= %s")
                params.append(max_rating)

            joins_sql = "\n".join(joins)
            where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

            # 1) count - используем DISTINCT f.id, чтобы не дублировались записи из-за JOIN
            count_sql = f"SELECT COUNT(DISTINCT f.id) FROM film f {joins_sql} {where_clause}"
            cur.execute(count_sql, tuple(params))
            total_count = cur.fetchone()[0] or 0

            # 2) select page
            sql = f"""
                SELECT f.id,
                       f.kinopoisk_id,
                       f.title,
                       f.original_title,
                       f.full_description,
                       f.poster,
                       f.year,
                       f.duration,
                       f.rating_kp,
                       f.rating_imdb
                FROM film f
                {joins_sql}
                {where_clause}
                ORDER BY f.id
                LIMIT %s OFFSET %s
            """
            # параметры для выборки — те же, плюс page_size и offset
            params_for_select = params.copy()
            params_for_select.extend([page_size, offset])
            cur.execute(sql, tuple(params_for_select))

            rows = cur.fetchall()
            items = [
                {
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "title": r[2],
                    "original_title": r[3],
                    "full_description": r[4],
                    "poster": r[5],
                    "year": r[6],
                    "duration": r[7],
                    "rating_kp": r[8],
                    "rating_imdb": r[9],
                }
                for r in rows
            ]
            return {"items": items, "page": page, "page_size": page_size, "total_count": total_count}
        finally:
            cur.close()


@router.get("/{film_id}", summary="Детали фильма")
def get_film(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT id,
                       kinopoisk_id,
                       title,
                       original_title,
                       description,
                       full_description,
                       poster,
                       year,
                       tagline,
                       ru_premiere,
                       world_premiere,
                       content_rating,
                       is_family_friendly,
                       duration,
                       rating_kp,
                       kp_votes_count,
                       rating_imdb,
                       imdb_votes_count,
                       budget,
                       usa_box_office,
                       rus_box_office,
                       user_rating,
                       user_rating_count
                FROM film
                WHERE id=%s
                """,
                (film_id,)
            )
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
                "tagline": r[8],
                "ru_premiere": r[9],
                "world_premiere": r[10],
                "content_rating": r[11],
                "isFamilyFriendly": r[12],
                "duration": r[13],
                "rating_kp": r[14],
                "kp_votes_count": r[15],
                "rating_imdb": r[16],
                "imdb_votes_count": r[17],
                "budget": r[18],
                "usa_box_office": r[19],
                "rus_box_office": r[20],
                "user_rating": float(r[21]) if r[21] else None,
                "user_rating_count": r[22],
            }
        finally:
            cur.close()


@router.get("/kinopoisk/{kinopoisk_id}", summary="Получить фильм по Кинопоиск ID")
def get_film_by_kinopoisk_id(kinopoisk_id: str):
    """Получает фильм по его Кинопоиск ID"""
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT id,
                       kinopoisk_id,
                       title,
                       original_title,
                       description,
                       full_description,
                       poster,
                       year,
                       tagline,
                       ru_premiere,
                       world_premiere,
                       content_rating,
                       is_family_friendly,
                       duration,
                       rating_kp,
                       kp_votes_count,
                       rating_imdb,
                       imdb_votes_count,
                       budget,
                       usa_box_office,
                       rus_box_office,
                       user_rating,
                       user_rating_count
                FROM film
                WHERE kinopoisk_id = %s
                """,
                (kinopoisk_id,)
            )
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
                "tagline": r[8],
                "ru_premiere": r[9],
                "world_premiere": r[10],
                "content_rating": r[11],
                "isFamilyFriendly": r[12],
                "duration": r[13],
                "rating_kp": r[14],
                "kp_votes_count": r[15],
                "rating_imdb": r[16],
                "imdb_votes_count": r[17],
                "budget": r[18],
                "usa_box_office": r[19],
                "rus_box_office": r[20],
                "user_rating": float(r[21]) if r[21] else None,
                "user_rating_count": r[22],
            }
        finally:
            cur.close()


@router.get("/{film_id}/watch-providers", summary="Где смотреть (провайдеры)")
def get_watch_providers(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT name, url, logo
                FROM film_watch_provider
                WHERE film_id = %s
                ORDER BY name
                """,
                (film_id,)
            )
            rows = cur.fetchall()
            return [
                {"name": r[0], "url": r[1], "logo": r[2]}
                for r in rows
            ]
        finally:
            cur.close()

@router.get("/{film_id}/similar", summary="Похожие фильмы (расширенные)")
def get_similar_films(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT similar_film_id, similar_film_title, similar_film_year,
                       similar_film_genres, similar_film_poster, similar_film_rating
                FROM similar_film
                WHERE film_id=%s
                ORDER BY id
                """,
                (film_id,)
            )
            rows = cur.fetchall()
            items = []
            for r in rows:
                items.append({
                    "kinopoisk_id": r[0],
                    "title": r[1],
                    "year": r[2],
                    "genres": r[3],
                    "poster": r[4],
                    "rating": r[5],
                })
            return items
        finally:
            cur.close()


@router.get("/{film_id}/recommendations", summary="Рекомендуемые фильмы на основе контентной фильтрации")
def get_film_recommendations(film_id: int, limit: int = Query(10, ge=1, le=50, description="Количество рекомендаций")):
    """
    Система рекомендаций на основе:
    - Жанры (40%)
    - Участники (30%) 
    - Год выпуска (15%)
    - Рейтинг (15%)
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            # Получаем данные текущего фильма
            cur.execute("""
                SELECT f.id, f.year, f.rating_kp, f.title, f.poster, f.kinopoisk_id
                FROM film f WHERE f.id = %s
            """, (film_id,))
            
            current_film = cur.fetchone()
            if not current_film:
                return []
            
            current_year = current_film[1]
            current_rating = current_film[2]
            
            # Получаем жанры текущего фильма
            cur.execute("""
                SELECT g.name FROM film_genre fg
                JOIN genre g ON g.id = fg.genre_id
                WHERE fg.film_id = %s
            """, (film_id,))
            current_genres = [row[0] for row in cur.fetchall()]
            
            # Получаем участников текущего фильма
            cur.execute("""
                SELECT fs.stuff_id FROM film_stuff fs
                WHERE fs.film_id = %s
            """, (film_id,))
            current_stuff_ids = [row[0] for row in cur.fetchall()]
            
            # Получаем кандидатов для рекомендаций (исключаем текущий фильм)
            cur.execute("""
                SELECT DISTINCT f.id, f.title, f.year, f.rating_kp, f.poster, f.kinopoisk_id,
                       f.description, f.original_title
                FROM film f
                WHERE f.id != %s AND f.title IS NOT NULL
                ORDER BY f.rating_kp DESC NULLS LAST
                LIMIT 200
            """, (film_id,))
            
            candidates = cur.fetchall()
            recommendations = []
            
            for candidate in candidates:
                candidate_id = candidate[0]
                candidate_year = candidate[2]
                candidate_rating = candidate[3]
                
                # Подсчет совпадений по жанрам (40%)
                cur.execute("""
                    SELECT COUNT(*) FROM film_genre fg1
                    JOIN film_genre fg2 ON fg1.genre_id = fg2.genre_id
                    WHERE fg1.film_id = %s AND fg2.film_id = %s
                """, (film_id, candidate_id))
                genre_matches = cur.fetchone()[0]
                genre_score = (genre_matches / max(len(current_genres), 1)) * 0.4 if current_genres else 0
                
                # Подсчет совпадений по участникам (30%)
                cur.execute("""
                    SELECT COUNT(*) FROM film_stuff fs1
                    JOIN film_stuff fs2 ON fs1.stuff_id = fs2.stuff_id
                    WHERE fs1.film_id = %s AND fs2.film_id = %s
                """, (film_id, candidate_id))
                stuff_matches = cur.fetchone()[0]
                stuff_score = (stuff_matches / max(len(current_stuff_ids), 1)) * 0.3 if current_stuff_ids else 0
                
                # Близость по году (15%)
                year_diff = abs((current_year or 0) - (candidate_year or 0))
                year_score = max(0, (10 - year_diff) / 10) * 0.15 if current_year and candidate_year else 0
                
                # Близость по рейтингу (15%)
                rating_diff = abs(float(current_rating or 0) - float(candidate_rating or 0))
                rating_score = max(0, (2 - rating_diff) / 2) * 0.15 if current_rating and candidate_rating else 0
                
                # Общий скор
                total_score = genre_score + stuff_score + year_score + rating_score
                
                if total_score > 0.1:  # Минимальный порог релевантности
                    recommendations.append({
                        "id": candidate[0],
                        "kinopoisk_id": candidate[5],
                        "title": candidate[1],
                        "original_title": candidate[7],
                        "year": candidate[2],
                        "rating_kp": candidate[3],
                        "poster": candidate[4],
                        "description": candidate[6],
                        "relevance_score": round(total_score, 3),
                        "genre_matches": genre_matches,
                        "stuff_matches": stuff_matches
                    })
            
            # Сортируем по релевантности и возвращаем топ
            recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
            return recommendations[:limit]
            
        finally:
            cur.close()


@router.get("/{film_id}/stills", summary="Кадры и обои фильма (оригиналы)")
def get_film_stills(film_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT picture_id, original_url, source
                FROM film_still
                WHERE film_id = %s
                ORDER BY source, picture_id
                """,
                (film_id,)
            )
            rows = cur.fetchall()
            grouped = {"stills": [], "wall": []}
            for r in rows:
                item = {"id": r[0], "original": r[1]}
                src = r[2]
                if src in grouped:
                    grouped[src].append(item)
            return grouped
        finally:
            cur.close()

@router.get("/{film_id}/stuff", summary="Список участников (stuff), участвовавших в фильме")
def get_film_stuff(film_id: int, role: str = Query("all", description="Роль участника (например: actor, director, writer). 'all' — без фильтра")):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            if role and role.lower() != "all":
                cur.execute(
                    """
                    SELECT s.id, s.kinopoisk_id, s.name, s.original_name, s.image, fs.role
                    FROM film_stuff fs
                    JOIN stuff s ON s.id = fs.stuff_id
                    WHERE fs.film_id = %s AND fs.role = %s
                    ORDER BY s.id
                    """,
                    (film_id, role)
                )
            else:
                cur.execute(
                    """
                    SELECT s.id, s.kinopoisk_id, s.name, s.original_name, s.image, fs.role
                    FROM film_stuff fs
                    JOIN stuff s ON s.id = fs.stuff_id
                    WHERE fs.film_id = %s
                    ORDER BY s.id
                    """,
                    (film_id,)
                )
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "kinopoisk_id": r[1],
                    "name": r[2],
                    "original_name": r[3],
                    "image": r[4],
                    "role": r[5],
                }
                for r in rows
            ]
        finally:
            cur.close()
