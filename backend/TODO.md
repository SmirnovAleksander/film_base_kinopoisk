F841 Local variable `total_count` is assigned to but never used
  --> fastapi-application\api\api_v1\admin\films.py:55:5
   |
53 |     total_count_stmt = select(func.count(Film.id))
54 |     total_count_result = await session.execute(total_count_stmt)
55 |     total_count = total_count_result.scalar()
   |     ^^^^^^^^^^^
56 |
57 |     # Получаем фильмы для текущей страницы
   |
help: Remove assignment to unused variable `total_count`

E712 Avoid equality comparisons to `False`; use `not Comment.is_deleted:` for false checks
  --> fastapi-application\api\api_v1\comments.py:37:17
   |
35 |             and_(
36 |                 Comment.film_id == film_id,
37 |                 Comment.is_deleted == False
   |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
38 |             )
39 |         )
   |
help: Replace with `not Comment.is_deleted`

F401 `.access_tokens.get_access_token_db` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> fastapi-application\api\dependencies\authentification\__init__.py:9:28
   |
 7 | )
 8 |
 9 | from .access_tokens import get_access_token_db
   |                            ^^^^^^^^^^^^^^^^^^^
10 | from .backend import auth_backend
11 | from .strategy import get_database_strategy
   |
help: Add unused import `get_access_token_db` to __all__

F401 `.backend.auth_backend` imported but unused; consider removing, adding to `__all__`, or using a redundant alias    
  --> fastapi-application\api\dependencies\authentification\__init__.py:10:22
   |
 9 | from .access_tokens import get_access_token_db
10 | from .backend import auth_backend
   |                      ^^^^^^^^^^^^
11 | from .strategy import get_database_strategy
12 | from .user_manager import get_user_manager
   |
help: Add unused import `auth_backend` to __all__

F401 `.strategy.get_database_strategy` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> fastapi-application\api\dependencies\authentification\__init__.py:11:23
   |
 9 | from .access_tokens import get_access_token_db
10 | from .backend import auth_backend
11 | from .strategy import get_database_strategy
   |                       ^^^^^^^^^^^^^^^^^^^^^
12 | from .user_manager import get_user_manager
13 | from .users import get_user_db
   |
help: Add unused import `get_database_strategy` to __all__

F401 `.user_manager.get_user_manager` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> fastapi-application\api\dependencies\authentification\__init__.py:12:27
   |
10 | from .backend import auth_backend
11 | from .strategy import get_database_strategy
12 | from .user_manager import get_user_manager
   |                           ^^^^^^^^^^^^^^^^
13 | from .users import get_user_db
   |
help: Add unused import `get_user_manager` to __all__

F401 `.users.get_user_db` imported but unused; consider removing, adding to `__all__`, or using a redundant alias       
  --> fastapi-application\api\dependencies\authentification\__init__.py:13:20
   |
11 | from .strategy import get_database_strategy
12 | from .user_manager import get_user_manager
13 | from .users import get_user_db
   |                    ^^^^^^^^^^^
   |
help: Add unused import `get_user_db` to __all__

F401 `.associations.film_genre` imported but unused; consider removing, adding to `__all__`, or using a redundant alias 
  --> fastapi-application\core\models\__init__.py:24:27
   |
22 | from .film import Film, Genre, Country, Stuff, FilmStill, FilmWatchProvider, SimilarFilm
23 | from .user_interactions import Bookmark, Comment, UserFilmRating
24 | from .associations import film_genre, film_country, film_stuff
   |                           ^^^^^^^^^^
   |
help: Add unused import `film_genre` to __all__

F401 `.associations.film_country` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> fastapi-application\core\models\__init__.py:24:39
   |
22 | from .film import Film, Genre, Country, Stuff, FilmStill, FilmWatchProvider, SimilarFilm
23 | from .user_interactions import Bookmark, Comment, UserFilmRating
24 | from .associations import film_genre, film_country, film_stuff
   |                                       ^^^^^^^^^^^^
   |
help: Add unused import `film_country` to __all__

F401 `.associations.film_stuff` imported but unused; consider removing, adding to `__all__`, or using a redundant alias 
  --> fastapi-application\core\models\__init__.py:24:53
   |
22 | from .film import Film, Genre, Country, Stuff, FilmStill, FilmWatchProvider, SimilarFilm
23 | from .user_interactions import Bookmark, Comment, UserFilmRating
24 | from .associations import film_genre, film_country, film_stuff
   |                                                     ^^^^^^^^^^
   |
help: Add unused import `film_stuff` to __all__