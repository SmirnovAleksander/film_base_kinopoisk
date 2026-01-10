import psycopg2
import time
from parser_utils.kinopoisk_parser import KinopoiskParser
from parser_utils.film_page_parser import FilmPageParser
from parser_utils.serial_page_parser import SerialPageParser
from parser_utils.stuff_page_parser import ActorPageParser
from parser_utils.film_series_images_parser import FilmImagesParser
from parser_utils.stuff_images_parser import StuffImagesParser
from parser_utils.stuff_filmography_parser import StuffFilmographyParser
from config import DATABASE_CONFIG, DELAYS, PARSING_CONFIG, LOGGING_CONFIG


class MainParser:
    def __init__(self):
        """Инициализация главного парсера"""
        # Используем конфигурацию из config.py
        self.db_config = DATABASE_CONFIG
        self.delays = DELAYS
        self.parsing_config = PARSING_CONFIG
        self.logging_config = LOGGING_CONFIG
        
        # Инициализируем парсеры
        self.kinopoisk_parser = KinopoiskParser()
        self.film_parser = FilmPageParser()
        self.serial_parser = SerialPageParser()
        self.actor_parser = ActorPageParser()
        self.images_parser = FilmImagesParser()
        self.stuff_images_parser = StuffImagesParser()
        self.stuff_filmography_parser = StuffFilmographyParser()
        

        
        # Подключаемся к БД
        self.db_connection = self.connect_to_db()
        self.create_tables()
        
        # Отслеживаем уже спарсенных участников
        self.parsed_people = set()
        
    def connect_to_db(self):
        """Подключение к PostgreSQL"""
        try:
            connection = psycopg2.connect(**self.db_config)
            print("✅ Подключение к PostgreSQL успешно")
            return connection
        except Exception as e:
            print(f"❌ Ошибка подключения к БД: {e}")
            return None
    
    def create_tables(self):
        """Создание таблиц в БД"""
        if not self.db_connection:
            return
            
        cursor = self.db_connection.cursor()
        
        # Создаем таблицы для парсинга данных
        tables = [
            """
            CREATE TABLE IF NOT EXISTS film (
                id SERIAL PRIMARY KEY,
                kinopoisk_id VARCHAR(20) UNIQUE NOT NULL,
                title_ru VARCHAR(500),
                title_en VARCHAR(500),
                description_short TEXT,
                description_full TEXT,
                poster_url VARCHAR(1000),
                release_year INTEGER,
                tagline TEXT,
                premiere_ru VARCHAR(100),
                premiere_world VARCHAR(100),
                content_type VARCHAR(50),
                is_family BOOLEAN DEFAULT FALSE,
                duration VARCHAR(50),
                rating_kp DECIMAL(3,1),
                votes_kp INTEGER,
                rating_imdb DECIMAL(3,1),
                votes_imdb INTEGER,
                rating_user DECIMAL(3,1),
                votes_user INTEGER DEFAULT 0,
                budget VARCHAR(100),
                box_office_usa VARCHAR(100),
                box_office_rus VARCHAR(100)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS stuff (
                id SERIAL PRIMARY KEY,
                kinopoisk_id VARCHAR(20) UNIQUE NOT NULL,
                name_ru VARCHAR(200),
                name_en VARCHAR(200),
                career TEXT[],
                genres TEXT[],
                height VARCHAR(50),
                zodiac VARCHAR(50),
                birth_date VARCHAR(100),
                birth_place TEXT[],
                spouse TEXT[],
                children TEXT[],
                films_total INTEGER,
                career_start INTEGER,
                photo_url VARCHAR(1000)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS media (
                id SERIAL PRIMARY KEY,
                url VARCHAR(500) UNIQUE,
                title VARCHAR(1000),
                image_url VARCHAR(1000),
                category VARCHAR(100),
                publish_date VARCHAR(100),
                card_type VARCHAR(20),
                type VARCHAR(20) DEFAULT 'news',
                parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS genre (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS country (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS series (
                id SERIAL PRIMARY KEY,
                kinopoisk_id VARCHAR(20) UNIQUE NOT NULL,
                title_ru VARCHAR(500),
                title_en VARCHAR(500),
                description_short TEXT,
                description_full TEXT,
                poster_url VARCHAR(1000),
                release_year INTEGER,
                tagline TEXT,
                premiere_ru VARCHAR(100),
                premiere_world VARCHAR(100),
                content_type VARCHAR(50),
                is_family BOOLEAN DEFAULT FALSE,
                rating_kp DECIMAL(3,1),
                votes_kp INTEGER,
                rating_imdb DECIMAL(3,1),
                votes_imdb INTEGER,
                rating_user DECIMAL(3,1),
                votes_user INTEGER DEFAULT 0,
                platform VARCHAR(200),
                episodes_count INTEGER
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_genre (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                genre_id INTEGER REFERENCES genre(id),
                UNIQUE(content_id, content_type, genre_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_country (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                country_id INTEGER REFERENCES country(id),
                UNIQUE(content_id, content_type, country_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_stuff (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                stuff_id INTEGER REFERENCES stuff(id),
                role VARCHAR(100),
                UNIQUE(content_id, content_type, stuff_id, role)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS similar_content (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                similar_id VARCHAR(20) NOT NULL,
                similar_type VARCHAR(20) NOT NULL CHECK (similar_type IN ('film', 'series')),
                title_ru VARCHAR(500),
                release_year INTEGER,
                genres TEXT[],
                poster_url TEXT,
                rating_kp DECIMAL(3,1),
                UNIQUE(content_id, content_type, similar_id, similar_type)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_images (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                picture_id VARCHAR(20) NOT NULL,
                image_url TEXT NOT NULL,
                image_type VARCHAR(50) NOT NULL,
                UNIQUE(content_id, content_type, picture_id, image_type)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_watch_provider (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                provider_name VARCHAR(200) NOT NULL,
                provider_url TEXT NOT NULL,
                provider_logo TEXT NULL,
                UNIQUE(content_id, content_type, provider_name)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS stuff_images (
                id SERIAL PRIMARY KEY,
                stuff_id INTEGER NOT NULL REFERENCES stuff(id) ON DELETE CASCADE,
                picture_id VARCHAR(20) NOT NULL,
                image_url TEXT NOT NULL,
                image_type VARCHAR(50) NOT NULL,
                UNIQUE(stuff_id, picture_id, image_type)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS stuff_filmography (
                id SERIAL PRIMARY KEY,
                stuff_id INTEGER NOT NULL REFERENCES stuff(id) ON DELETE CASCADE,
                content_id VARCHAR(20) NOT NULL,
                title_ru VARCHAR(500),
                title_en VARCHAR(500),
                release_year INTEGER,
                genres TEXT,
                countries TEXT,
                poster_url VARCHAR(1000),
                rating_kp DECIMAL(3,1),
                votes_kp INTEGER,
                role VARCHAR(100),
                release_year_start INTEGER,
                release_year_end INTEGER,
                UNIQUE(stuff_id, content_id, role)
            )
            """
        ]
        
        try:
            for table_sql in tables:
                cursor.execute(table_sql)
            self.db_connection.commit()
            print("✅ Таблицы созданы успешно")
        except Exception as e:
            print(f"❌ Ошибка создания таблиц: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()
    
    def parse_all_films(self, start_page=1, max_pages=5):
        """Парсинг всех фильмов с нескольких страниц"""
        # Старт парсинга
        
        for page in range(start_page, start_page + max_pages):
            # Парсинг страницы
            
            # URL страницы со списком фильмов
            if page == 1:
                page_url = "https://www.kinopoisk.ru/lists/movies/top250/"
            else:
                page_url = f"https://www.kinopoisk.ru/lists/movies/top250/?page={page}"
            
            try:
                # Парсим список фильмов
                self.kinopoisk_parser.load_html_from_url(page_url)
                film_ids = self.kinopoisk_parser.parse_all_films()
                # Единый вывод: количество найденных фильмов на странице
                print(f"📊 Найдено {len(film_ids)} фильмов на странице {page}")
                
                # Парсим каждый фильм
                for i, film_data in enumerate(film_ids, 1):
                    film_id = film_data.get('id')
                    if not film_id:
                        continue
                        
                    # Парсим детали фильма
                    film_details = self.parse_film_details(film_id)
                    if film_details:
                        # Показываем название фильма перед парсингом актеров
                        film_title = film_details.get('title', 'Unknown Film')
                        print(f"🎬 Парсинг фильма: {film_title}")

                        # Сохраняем фильм в БД
                        film_db_id = self.save_film_to_db(film_details)
                        
                        # Парсим всех участников фильма
                        self.parse_film_people(film_id, film_db_id, film_details)
                        
                        # Парсим похожие фильмы
                        self.parse_similar_content(film_details, film_db_id, 'film')

                        # Парсим кадры (stills + wall)
                        self.parse_and_save_stills(film_id, film_db_id, 'film')
                        
                        # Тихий режим
                        print(f"✅ Фильм '{film_title}' полностью обработан")
                    
                    # Пауза между запросами
                    time.sleep(self.delays['BETWEEN_FILMS'])
                    
            except Exception as e:
                print(f"❌ Ошибка парсинга страницы {page}: {e}")
                continue
            
            # Пауза между страницами (кроме последней)
            if page < start_page + max_pages - 1:
                # Тихий режим
                time.sleep(self.delays['BETWEEN_PAGES'])
        # Завершение без лишнего вывода
    
    def parse_all_series(self, start_page=1, max_pages=5):
        """Парсинг всех сериалов с нескольких страниц"""
        for page in range(start_page, start_page + max_pages):
            # URL страницы со списком сериалов
            if page == 1:
                page_url = "https://www.kinopoisk.ru/lists/movies/series-top250/?b=top"
            else:
                page_url = f"https://www.kinopoisk.ru/lists/movies/series-top250/?b=top&page={page}"
            
            try:
                # Парсим список сериалов
                self.kinopoisk_parser.load_html_from_url(page_url)
                series_ids = self.kinopoisk_parser.parse_all_series()
                print(f"📊 Найдено {len(series_ids)} сериалов на странице {page}")
                
                # Парсим каждый сериал
                for i, series_data in enumerate(series_ids, 1):
                    series_id = series_data.get('id')
                    if not series_id:
                        continue
                        
                    # Парсим детали сериала
                    series_details = self.parse_series_details(series_id)
                    if series_details:
                        # Показываем название сериала перед парсингом актеров
                        series_title = series_details.get('title', 'Unknown Series')
                        print(f"📺 Парсинг сериала: {series_title}")

                        # Сохраняем сериал в БД
                        series_db_id = self.save_series_to_db(series_details)
                        
                        # Парсим всех участников сериала
                        self.parse_series_people(series_id, series_db_id, series_details)
                        
                        # Парсим похожие сериалы/фильмы
                        self.parse_similar_content(series_details, series_db_id, 'series')

                        # Парсим кадры (stills + wall)
                        self.parse_and_save_stills(series_id, series_db_id, 'series')
                        
                        print(f"✅ Сериал '{series_title}' полностью обработан")
                    
                    # Пауза между запросами
                    time.sleep(self.delays['BETWEEN_FILMS'])
                    
            except Exception as e:
                print(f"❌ Ошибка парсинга страницы {page}: {e}")
                continue
            
            # Пауза между страницами (кроме последней)
            if page < start_page + max_pages - 1:
                time.sleep(self.delays['BETWEEN_PAGES'])
    
    def parse_film_details(self, film_id):
        """Парсинг детальной страницы фильма"""
        try:
            film_url = f"https://kinopoisk.ru/film/{film_id}/"
            self.film_parser.load_html_from_url(film_url)
            film_data = self.film_parser.extract_film_details()
            
            # Добавляем ID фильма
            film_data['kinopoisk_id'] = film_id
            
            return film_data
        except Exception as e:
            print(f"❌ Ошибка парсинга фильма {film_id}: {e}")
            return None
    
    def parse_series_details(self, series_id):
        """Парсинг детальной страницы сериала"""
        try:
            series_url = f"https://kinopoisk.ru/series/{series_id}/"
            self.serial_parser.load_html_from_url(series_url)
            series_data = self.serial_parser.extract_film_details()
            
            # Добавляем ID сериала
            series_data['kinopoisk_id'] = series_id
            
            return series_data
        except Exception as e:
            print(f"❌ Ошибка парсинга сериала {series_id}: {e}")
            return None
    
    def parse_film_people(self, film_id, film_db_id, film_data):
        """Парсинг всех участников фильма"""
        film_title = film_data.get('title', 'Unknown Film')

        people_roles = [
            ('actors', 'actor'),
            ('directors', 'director'),
            ('producers', 'producer'),
        ]
        
        for role_key, role_name in people_roles:
            people_list = film_data.get(role_key, [])
            if not people_list:
                continue
                
            print(f"  👥 Парсинг {role_name}s ({len(people_list)} человек) для фильма '{film_title}'")
            
            for person_data in people_list:
                person_id = person_data.get('id')
                if not person_id:
                    continue

                person_db_id = None

                # Если участник уже парсился ранее, не парсим заново, а пытаемся получить его id из БД
                if person_id in self.parsed_people:
                    person_db_id = self.get_person_db_id(person_id)
                    # На случай, если по какой-то причине в БД его нет — пробуем всё же спарсить и сохранить
                    if not person_db_id:
                        person_details = self.parse_person_details(person_id)
                        if person_details:
                            person_db_id = self.save_person_to_db(person_details)
                else:
                    # Парсим детали участника впервые
                    person_details = self.parse_person_details(person_id)
                    if person_details:
                        person_db_id = self.save_person_to_db(person_details)
                        # Парсим изображения участника
                        self.parse_and_save_stuff_images(person_id, person_db_id)
                        # Парсим фильмографию участника
                        self.parse_and_save_stuff_filmography(person_id, person_db_id)

                        # Отмечаем как спарсенного, чтобы больше не ходить на страницу актёра
                        self.parsed_people.add(person_id)

                # Если удалось получить/создать участника в БД — всегда создаём связь фильм–участник
                if person_db_id:
                    self.save_content_person_relation(film_db_id, 'film', person_db_id, role_name)
                    print(f"✅ {role_name}: {person_data.get('name', 'Unknown')}")
                
                # Пауза между запросами
                time.sleep(self.delays['BETWEEN_PEOPLE'])
    
    def parse_series_people(self, series_id, series_db_id, series_data):
        """Парсинг всех участников сериала"""
        series_title = series_data.get('title', 'Unknown Series')

        people_roles = [
            ('actors', 'actor'),
            ('directors', 'director'),
            ('producers', 'producer'),
        ]
        
        for role_key, role_name in people_roles:
            people_list = series_data.get(role_key, [])
            if not people_list:
                continue
                
            print(f"  👥 Парсинг {role_name}s ({len(people_list)} человек) для сериала '{series_title}'")
            
            for person_data in people_list:
                person_id = person_data.get('id')
                if not person_id:
                    continue

                person_db_id = None

                # Если участник уже парсился ранее, не парсим заново, а пытаемся получить его id из БД
                if person_id in self.parsed_people:
                    person_db_id = self.get_person_db_id(person_id)
                    if not person_db_id:
                        person_details = self.parse_person_details(person_id)
                        if person_details:
                            person_db_id = self.save_person_to_db(person_details)
                else:
                    # Парсим детали участника впервые
                    person_details = self.parse_person_details(person_id)
                    if person_details:
                        person_db_id = self.save_person_to_db(person_details)
                        
                        # Парсим изображения участника
                        self.parse_and_save_stuff_images(person_id, person_db_id)
                        # Парсим фильмографию участника
                        self.parse_and_save_stuff_filmography(person_id, person_db_id)
                        
                        self.parsed_people.add(person_id)

                # Если удалось получить/создать участника в БД — всегда создаём связь сериал–участник
                if person_db_id:
                    self.save_content_person_relation(series_db_id, 'series', person_db_id, role_name)
                    print(f"✅ {role_name}: {person_data.get('name', 'Unknown')}")
                
                # Пауза между запросами
                time.sleep(self.delays['BETWEEN_PEOPLE'])

    def get_person_db_id(self, kinopoisk_id):
        """Получить id участника в БД по его kinopoisk_id"""
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                "SELECT id FROM stuff WHERE kinopoisk_id = %s",
                (kinopoisk_id,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"❌ Ошибка получения участника из БД (kinopoisk_id={kinopoisk_id}): {e}")
            return None
        finally:
            cursor.close()
    
    def parse_person_details(self, person_id):
        """Парсинг детальной страницы участника"""
        try:
            person_url = f"https://kinopoisk.ru/name/{person_id}/"
            self.actor_parser.load_html_from_url(person_url)
            person_data = self.actor_parser.extract_actor_details()
            
            # Добавляем ID участника
            person_data['kinopoisk_id'] = person_id
            
            return person_data
        except Exception as e:
            print(f"❌ Ошибка парсинга участника {person_id}: {e}")
            return None
    
    def parse_similar_content(self, content_data, content_db_id, content_type):
        """Парсинг похожего контента (фильмов или сериалов)"""
        similar_items = content_data.get('similar_films', [])
        if not similar_items:
            return
            
        print(f"🔗 Парсинг похожего контента: {len(similar_items)}")
        
        for similar_item in similar_items:
            if similar_item.get('id') and similar_item.get('title'):
                # Определяем тип похожего контента по URL или другим признакам
                # По умолчанию считаем, что похожий контент того же типа
                similar_type = content_type  # Можно улучшить, анализируя данные
                self.save_similar_content_extended(content_db_id, content_type, similar_item, similar_type)
    
    def save_film_to_db(self, film_data):
        """Сохранение фильма в БД"""
        cursor = self.db_connection.cursor()
        
        try:
 
            
            # Вставляем фильм
            insert_film = """
            INSERT INTO film (kinopoisk_id, title_ru, title_en, description_short, description_full, 
                             poster_url, release_year, tagline, premiere_ru, premiere_world, content_type, is_family,
                             duration, rating_kp, votes_kp, rating_imdb, votes_imdb,
                             budget, box_office_usa, box_office_rus, rating_user, votes_user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (kinopoisk_id) DO UPDATE SET
                title_ru = EXCLUDED.title_ru,
                title_en = EXCLUDED.title_en,
                description_short = EXCLUDED.description_short,
                description_full = EXCLUDED.description_full,
                poster_url = EXCLUDED.poster_url,
                release_year = EXCLUDED.release_year,
                tagline = EXCLUDED.tagline,
                premiere_ru = EXCLUDED.premiere_ru,
                premiere_world = EXCLUDED.premiere_world,
                content_type = EXCLUDED.content_type,
                is_family = EXCLUDED.is_family,
                duration = EXCLUDED.duration,
                rating_kp = EXCLUDED.rating_kp,
                votes_kp = EXCLUDED.votes_kp,
                rating_imdb = EXCLUDED.rating_imdb,
                votes_imdb = EXCLUDED.votes_imdb,
                budget = EXCLUDED.budget,
                box_office_usa = EXCLUDED.box_office_usa,
                box_office_rus = EXCLUDED.box_office_rus,
                rating_user = EXCLUDED.rating_user,
                votes_user = EXCLUDED.votes_user
            RETURNING id
            """
            
            cursor.execute(insert_film, (
                film_data.get('kinopoisk_id'),
                film_data.get('title'),
                film_data.get('original_title'),
                film_data.get('short_description'),
                film_data.get('description'),
                film_data.get('poster'),
                film_data.get('published_year'),
                film_data.get('tagline'),
                film_data.get('ru_premiere'),
                film_data.get('world_premiere'),
                film_data.get('content_type'),
                film_data.get('is_family_friendly', False),
                film_data.get('duration'),
                film_data.get('rating_kp'),
                film_data.get('kp_votes_count'),
                film_data.get('rating_imdb'),
                film_data.get('imdb_votes_count'),
                film_data.get('budget'),
                film_data.get('usa_box_office'),
                film_data.get('rus_box_office'),
                None,  # rating_user
                0      # votes_user
            ))
            
            film_db_id = cursor.fetchone()[0]
            
            # Сохраняем жанры
            self.save_content_genres(film_db_id, 'film', film_data.get('genres', []))
            
            # Сохраняем страны
            self.save_content_countries(film_db_id, 'film', film_data.get('countries', []))

            # Сохраняем провайдеров просмотра
            self.save_content_watch_providers(film_db_id, 'film', film_data.get('watch_providers', []))
            
            self.db_connection.commit()
            return film_db_id
            
        except Exception as e:
            print(f"❌ Ошибка сохранения фильма: {e}")
            self.db_connection.rollback()
            return None
        finally:
            cursor.close()

    def save_series_to_db(self, series_data):
        """Сохранение сериала в БД"""
        cursor = self.db_connection.cursor()
        
        try:
            # Вставляем сериал
            insert_series = """
            INSERT INTO series (kinopoisk_id, title_ru, title_en, description_short, description_full, 
                             poster_url, release_year, tagline, premiere_ru, premiere_world, content_type, is_family,
                             rating_kp, votes_kp, rating_imdb, votes_imdb,
                             rating_user, votes_user, platform, episodes_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (kinopoisk_id) DO UPDATE SET
                title_ru = EXCLUDED.title_ru,
                title_en = EXCLUDED.title_en,
                description_short = EXCLUDED.description_short,
                description_full = EXCLUDED.description_full,
                poster_url = EXCLUDED.poster_url,
                release_year = EXCLUDED.release_year,
                tagline = EXCLUDED.tagline,
                premiere_ru = EXCLUDED.premiere_ru,
                premiere_world = EXCLUDED.premiere_world,
                content_type = EXCLUDED.content_type,
                is_family = EXCLUDED.is_family,
                rating_kp = EXCLUDED.rating_kp,
                votes_kp = EXCLUDED.votes_kp,
                rating_imdb = EXCLUDED.rating_imdb,
                votes_imdb = EXCLUDED.votes_imdb,
                rating_user = EXCLUDED.rating_user,
                votes_user = EXCLUDED.votes_user,
                platform = EXCLUDED.platform,
                episodes_count = EXCLUDED.episodes_count
            RETURNING id
            """
            
            cursor.execute(insert_series, (
                series_data.get('kinopoisk_id'),
                series_data.get('title'),
                series_data.get('original_title'),
                series_data.get('short_description'),
                series_data.get('description'),
                series_data.get('poster'),
                series_data.get('published_year'),
                series_data.get('tagline'),
                series_data.get('ru_premiere'),
                series_data.get('world_premiere'),
                series_data.get('content_type'),
                series_data.get('is_family_friendly', False),
                series_data.get('rating_kp'),
                series_data.get('kp_votes_count'),
                series_data.get('rating_imdb'),
                series_data.get('imdb_votes_count'),
                None,  # rating_user
                0,     # votes_user
                series_data.get('platform'),
                series_data.get('number_of_episodes')
            ))
            
            series_db_id = cursor.fetchone()[0]
            
            # Сохраняем жанры
            self.save_content_genres(series_db_id, 'series', series_data.get('genres', []))
            
            # Сохраняем страны
            self.save_content_countries(series_db_id, 'series', series_data.get('countries', []))

            # Сохраняем провайдеров просмотра
            self.save_content_watch_providers(series_db_id, 'series', series_data.get('watch_providers', []))
            
            self.db_connection.commit()
            return series_db_id
            
        except Exception as e:
            print(f"❌ Ошибка сохранения сериала: {e}")
            self.db_connection.rollback()
            return None
        finally:
            cursor.close()

    def save_content_watch_providers(self, content_db_id, content_type, providers):
        """Сохранение провайдеров просмотра контента (фильма или сериала)"""
        if not providers:
            return
        cursor = self.db_connection.cursor()
        try:
            for p in providers:
                name = p.get('name')
                url = p.get('url')
                logo = p.get('logo')
                if not name or not url:
                    continue
                cursor.execute(
                    """
                    INSERT INTO content_watch_provider (content_id, content_type, provider_name, provider_url, provider_logo)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (content_id, content_type, provider_name) DO UPDATE SET
                        provider_url = EXCLUDED.provider_url,
                        provider_logo = EXCLUDED.provider_logo
                    """,
                    (content_db_id, content_type, name, url, logo)
                )
        except Exception as e:
            print(f"❌ Ошибка сохранения провайдеров: {e}")
        finally:
            cursor.close()

    def parse_and_save_stills(self, content_kinopoisk_id: str, content_db_id: int, content_type: str):
        """Парсит кадры контента (фильма или сериала) через GraphQL API"""
        try:
            # Используем новый FilmImagesParser для получения изображений через GraphQL
            # Для фильмов и сериалов используем разные типы изображений
            image_types = ["STILL", "SHOOTING", "POSTER"]
            grouped = {}
            
            print(f"📸 Парсинг изображений для {content_type} {content_kinopoisk_id}")
            
            for image_type in image_types:
                try:
                    # Получаем изображения через GraphQL API
                    images = self.images_parser.fetch_movie_images_paginated(content_kinopoisk_id, image_type)
                    grouped[image_type.lower()] = images if images else []
                    print(f"  ✅ Спарсено {len(images) if images else 0} изображений типа '{image_type}'")
                except Exception as e:
                    print(f"  ⚠️ Не удалось спарсить изображения типа {image_type}: {e}")
                    grouped[image_type.lower()] = []
                    continue
                
                # Пауза между типами изображений
                time.sleep(self.delays['BETWEEN_FILMS'])
            
            # Сохраняем все изображения в БД
            self.save_content_images(content_db_id, content_type, grouped)
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге изображений {content_type} {content_kinopoisk_id}: {e}")

    def save_content_images(self, content_db_id: int, content_type: str, grouped_items):
        """Сохраняет кадры контента (фильма или сериала) в таблицу content_images с указанием типа."""
        cursor = self.db_connection.cursor()
        try:
            total_saved = 0
            total_errors = 0
            
            for image_type, images in grouped_items.items():
                for image_data in images:
                    picture_id = image_data.get('id')
                    image_url = image_data.get('original')
                    
                    if not picture_id or not image_url:
                        continue
                    
                    # Используем тип изображения напрямую в поле image_type
                    image_type = image_type
                    
                    try:
                        # Начинаем новую транзакцию для каждого кадра
                        cursor.execute(
                            """
                            INSERT INTO content_images (content_id, content_type, picture_id, image_url, image_type)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (content_id, content_type, picture_id, image_type) DO UPDATE SET
                                image_url = EXCLUDED.image_url
                            """,
                            (content_db_id, content_type, picture_id, image_url, image_type)
                        )
                        self.db_connection.commit()
                        total_saved += 1
                        
                    except Exception as e:
                        # Откатываем неудачную транзакцию и продолжаем
                        self.db_connection.rollback()
                        print(f"⚠️ Ошибка сохранения кадра {picture_id} (тип: {image_type}): {e}")
                        total_errors += 1
                        # Продолжаем с следующим кадром
                        continue
            
            if total_errors > 0:
                print(f"💾 Сохранено {total_saved} кадров в БД, {total_errors} ошибок")
            else:
                print(f"💾 Сохранено {total_saved} кадров в БД")
                
        except Exception as e:
            print(f"❌ Общая ошибка сохранения кадров: {e}")
            try:
                self.db_connection.rollback()
            except:
                pass
        finally:
            cursor.close()
    
    def parse_and_save_stuff_images(self, person_kinopoisk_id: str, person_db_id: int):
        """Парсит и сохраняет изображения персоны"""
        try:
            print(f"📸 Парсинг изображений для персоны {person_kinopoisk_id}")
            
            # Получаем изображения через GraphQL API
            # fetch_all_image_types возвращает список словарей [{'id': ..., 'original': ..., 'type': ...}, ...]
            images = self.stuff_images_parser.fetch_all_image_types(person_kinopoisk_id)
            
            if not images:
                print(f"  ⚠️ Изображения не найдены")
                return

            print(f"  ✅ Спарсено {len(images)} изображений")
            
            # Сохраняем изображения в БД
            self.save_stuff_images(person_db_id, images)
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге изображений персоны {person_kinopoisk_id}: {e}")

    def save_stuff_images(self, person_db_id: int, images):
        """Сохраняет изображения персоны в таблицу stuff_images"""
        cursor = self.db_connection.cursor()
        try:
            total_saved = 0
            total_errors = 0
            
            for image_data in images:
                picture_id = image_data.get('id')
                image_url = image_data.get('original')
                image_type = image_data.get('type')  # photo
                
                if not picture_id or not image_url:
                    continue
                
                try:
                    cursor.execute(
                        """
                        INSERT INTO stuff_images (stuff_id, picture_id, image_url, image_type)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (stuff_id, picture_id, image_type) DO UPDATE SET
                            image_url = EXCLUDED.image_url
                        """,
                        (person_db_id, picture_id, image_url, image_type)
                    )
                    self.db_connection.commit()
                    total_saved += 1
                    
                except Exception as e:
                    self.db_connection.rollback()
                    print(f"⚠️ Ошибка сохранения изображения персоны {picture_id}: {e}")
                    total_errors += 1
                    continue
            
            if total_errors > 0:
                print(f"💾 Сохранено {total_saved} изображений персоны в БД, {total_errors} ошибок")
            else:
                print(f"💾 Сохранено {total_saved} изображений персоны в БД")
                
        except Exception as e:
            print(f"❌ Общая ошибка сохранения изображений персоны: {e}")
            try:
                self.db_connection.rollback()
            except:
                pass
        finally:
            cursor.close()

    def parse_and_save_stuff_filmography(self, person_kinopoisk_id: int, person_db_id: int):
        """Парсит и сохраняет фильмографию персоны"""
        try:
            # print(f"🎥 Парсинг фильмографии для персоны {person_kinopoisk_id}")

            filmography_items = self.stuff_filmography_parser.fetch_stuff_filmography(person_kinopoisk_id, role_slugs=["ACTOR"])

            if not filmography_items:
                print(f"  ⚠️ Фильмография не найдена")
                return

            print(f"  ✅ Спарсено {len(filmography_items)} элементов фильмографии")

            self.save_stuff_filmography_to_db(person_db_id, filmography_items)

        except Exception as e:
            print(f"❌ Ошибка при парсинге фильмографии персоны {person_kinopoisk_id}: {e}")

    def save_stuff_filmography_to_db(self, person_db_id: int, filmography_items: list):
        """Сохраняет элементы фильмографии персоны в таблицу stuff_filmography"""
        cursor = self.db_connection.cursor()
        try:
            total_saved = 0
            total_errors = 0

            for item_data in filmography_items:
                try:
                    cursor.execute(
                        """
                        INSERT INTO stuff_filmography (
                            stuff_id, content_id, title_ru, title_en, release_year,
                            genres, countries, poster_url, rating_kp, votes_kp,
                            role, release_year_start, release_year_end
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (stuff_id, content_id, role) DO UPDATE SET
                            title_ru = EXCLUDED.title_ru,
                            title_en = EXCLUDED.title_en,
                            release_year = EXCLUDED.release_year,
                            genres = EXCLUDED.genres,
                            countries = EXCLUDED.countries,
                            poster_url = EXCLUDED.poster_url,
                            rating_kp = EXCLUDED.rating_kp,
                            votes_kp = EXCLUDED.votes_kp,
                            release_year_start = EXCLUDED.release_year_start,
                            release_year_end = EXCLUDED.release_year_end
                        """,
                        (
                            person_db_id,
                            item_data.get('movie_id'),
                            item_data.get('title'),
                            item_data.get('original_title'),
                            item_data.get('published_year'),
                            item_data.get('genres'),
                            item_data.get('countries'),
                            item_data.get('poster_url'),
                            item_data.get('rating_kinopoisk'),
                            item_data.get('rating_kinopoisk_count'),
                            item_data.get('role_slugs'),
                            item_data.get('release_year_start'),
                            item_data.get('release_year_end')
                        )
                    )
                    self.db_connection.commit()
                    total_saved += 1
                except Exception as e:
                    self.db_connection.rollback()
                    print(f"⚠️ Ошибка сохранения элемента фильмографии для фильма {item_data.get('movie_id')}: {e}")
                    total_errors += 1
                    continue

            if total_errors > 0:
                print(f"💾 Сохранено {total_saved} элементов фильмографии в БД, {total_errors} ошибок")
            else:
                print(f"💾 Сохранено {total_saved} элементов фильмографии в БД")

        except Exception as e:
            print(f"❌ Общая ошибка сохранения фильмографии: {e}")
            try:
                self.db_connection.rollback()
            except:
                pass
        finally:
            cursor.close()
    
    def save_person_to_db(self, person_data):
        """Сохранение участника в БД"""
        cursor = self.db_connection.cursor()
        
        try:
            # Вставляем участника
            insert_person = """
            INSERT INTO stuff (kinopoisk_id, name_ru, name_en, career, genres, height,
                                zodiac, birth_date, birth_place,
                                spouse, children, films_total, career_start,
                                photo_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (kinopoisk_id) DO UPDATE SET
                name_ru = EXCLUDED.name_ru,
                name_en = EXCLUDED.name_en,
                career = EXCLUDED.career,
                genres = EXCLUDED.genres,
                height = EXCLUDED.height,
                zodiac = EXCLUDED.zodiac,
                birth_date = EXCLUDED.birth_date,
                birth_place = EXCLUDED.birth_place,
                spouse = EXCLUDED.spouse,
                children = EXCLUDED.children,
                films_total = EXCLUDED.films_total,
                career_start = EXCLUDED.career_start,
                photo_url = EXCLUDED.photo_url
            RETURNING id
            """
            
            cursor.execute(insert_person, (
                person_data.get('kinopoisk_id'),
                person_data.get('name'),
                person_data.get('original_name'),
                person_data.get('career'),
                person_data.get('genres'),
                person_data.get('height'),
                person_data.get('zodiac'),
                person_data.get('birth_date'),
                person_data.get('birthplace'),
                person_data.get('spouse'),
                person_data.get('children'),
                person_data.get('total_films'),
                person_data.get('career_start_year'),
                person_data.get('image')
            ))
            
            person_db_id = cursor.fetchone()[0]
            
            self.db_connection.commit()
            return person_db_id
            
        except Exception as e:
            print(f"❌ Ошибка сохранения участника: {e}")
            self.db_connection.rollback()
            return None
        finally:
            cursor.close()
    
    def save_content_genres(self, content_db_id, content_type, genres):
        """Сохранение жанров контента (фильма или сериала)"""
        if not genres:
            return
            
        cursor = self.db_connection.cursor()
        
        try:
            for genre_name in genres:
                # Вставляем жанр
                cursor.execute(
                    "INSERT INTO genre (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (genre_name,)
                )
                
                # Получаем ID жанра
                cursor.execute("SELECT id FROM genre WHERE name = %s", (genre_name,))
                genre_id = cursor.fetchone()[0]
                
                # Создаем связь контент-жанр
                cursor.execute(
                    "INSERT INTO content_genre (content_id, content_type, genre_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (content_db_id, content_type, genre_id)
                )
                
        except Exception as e:
            print(f"❌ Ошибка сохранения жанров: {e}")
        finally:
            cursor.close()
    
    def save_content_countries(self, content_db_id, content_type, countries):
        """Сохранение стран контента (фильма или сериала)"""
        if not countries:
            return
            
        cursor = self.db_connection.cursor()
        
        try:
            for country_name in countries:
                # Вставляем страну
                cursor.execute(
                    "INSERT INTO country (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (country_name,)
                )
                
                # Получаем ID страны
                cursor.execute("SELECT id FROM country WHERE name = %s", (country_name,))
                country_id = cursor.fetchone()[0]
                
                # Создаем связь контент-страна
                cursor.execute(
                    "INSERT INTO content_country (content_id, content_type, country_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (content_db_id, content_type, country_id)
                )
                
        except Exception as e:
            print(f"❌ Ошибка сохранения стран: {e}")
        finally:
            cursor.close()
    
    def save_content_person_relation(self, content_db_id, content_type, person_db_id, role):
        """Создание связи контент-участник"""
        cursor = self.db_connection.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO content_stuff (content_id, content_type, stuff_id, role) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (content_db_id, content_type, person_db_id, role)
            )
        except Exception as e:
            print(f"❌ Ошибка создания связи контент-участник: {e}")
        finally:
            cursor.close()
    
    def save_similar_content_extended(self, content_db_id, content_type, similar_content, similar_content_type):
        """Сохранение похожего контента с расширенными полями"""
        cursor = self.db_connection.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO similar_content (
                    content_id, content_type, similar_id, similar_type,
                    title_ru, release_year, genres, poster_url, rating_kp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (content_id, content_type, similar_id, similar_type) DO UPDATE SET
                    title_ru = EXCLUDED.title_ru,
                    release_year = EXCLUDED.release_year,
                    genres = EXCLUDED.genres,
                    poster_url = EXCLUDED.poster_url,
                    rating_kp = EXCLUDED.rating_kp
                """,
                (
                    content_db_id,
                    content_type,
                    similar_content.get('id'),
                    similar_content_type,
                    similar_content.get('title'),
                    similar_content.get('year'),
                    similar_content.get('genres'),
                    similar_content.get('poster'),
                    similar_content.get('rating'),
                )
            )
        except Exception as e:
            print(f"❌ Ошибка создания связи похожих контентов: {e}")
        finally:
            cursor.close()
    
    def save_media_to_db(self, media_list):
        """Сохраняет медиа контент в БД"""
        if not self.db_connection or not media_list:
            return
        
        cursor = self.db_connection.cursor()
        
        try:
            for media_item in media_list:
                # Проверяем, существует ли уже такой медиа контент
                cursor.execute(
                    "SELECT id FROM media WHERE url = %s",
                    (media_item.get('url'),)
                )
                
                if cursor.fetchone():
                    # Обновляем существующий медиа контент
                    cursor.execute("""
                        UPDATE media SET
                            title = %s,
                            image_url = %s,
                            category = %s,
                            publish_date = %s,
                            card_type = %s,
                            type = %s,
                            parsed_at = CURRENT_TIMESTAMP
                        WHERE url = %s
                    """, (
                        media_item.get('title'),
                        media_item.get('image_url'),
                        media_item.get('category'),
                        media_item.get('publish_date'),
                        media_item.get('card_type'),
                        media_item.get('type', 'news'),
                        media_item.get('url')
                    ))
                else:
                    # Вставляем новый медиа контент
                    cursor.execute("""
                        INSERT INTO media (url, title, image_url, category, publish_date, card_type, type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        media_item.get('url'),
                        media_item.get('title'),
                        media_item.get('image_url'),
                        media_item.get('category'),
                        media_item.get('publish_date'),
                        media_item.get('card_type'),
                        media_item.get('type', 'news')
                    ))
            
            self.db_connection.commit()
            print(f"✅ Сохранено {len(media_list)} медиа элементов в БД")
            
        except Exception as e:
            self.db_connection.rollback()
            print(f"❌ Ошибка сохранения медиа контента в БД: {e}")
        finally:
            cursor.close()
    
    def close_connection(self):
        """Закрытие соединения с БД"""
        if self.db_connection:
            self.db_connection.close()
            print("🔌 Соединение с БД закрыто")

def main():
    """Главная функция"""
    parser = MainParser()
    
    try:
        # Парсим все фильмы (начинаем с 1 страницы, максимум 3 страницы)
        parser.parse_all_films(start_page=1, max_pages=3)
        
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        parser.close_connection()

if __name__ == "__main__":
    main()
