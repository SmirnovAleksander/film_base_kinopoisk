import psycopg2
import time
from parser_utils.kinopoisk_parser import KinopoiskParser
from parser_utils.film_page_parser import FilmPageParser
from parser_utils.serial_page_parser import SerialPageParser
from parser_utils.actor_page_parser import ActorPageParser
from parser_utils.stills_page_parser import StillsPageParser
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
        self.stills_parser = StillsPageParser()
        

        
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
                title VARCHAR(500),
                original_title VARCHAR(500),
                description TEXT,
                full_description TEXT,
                poster VARCHAR(1000),
                year INTEGER,
                tagline TEXT,
                ru_premiere VARCHAR(100),
                world_premiere VARCHAR(100),
                content_rating VARCHAR(20),
                is_family_friendly BOOLEAN DEFAULT FALSE,
                duration VARCHAR(50),
                rating_kp DECIMAL(3,1),
                kp_votes_count VARCHAR(50),
                rating_imdb DECIMAL(3,1),
                imdb_votes_count VARCHAR(50),
                budget VARCHAR(100),
                usa_box_office VARCHAR(100),
                rus_box_office VARCHAR(100),
                user_rating DECIMAL(3,1),
                user_rating_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS stuff (
                id SERIAL PRIMARY KEY,
                kinopoisk_id VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(200),
                original_name VARCHAR(200),
                career TEXT[],
                ganres TEXT[],
                height VARCHAR(50),
                birthday_day_month VARCHAR(50),
                zodiac VARCHAR(50),
                age INTEGER,
                birthplace TEXT[],
                spouse TEXT[],
                children TEXT[],
                total_films INTEGER,
                career_start_year INTEGER,
                career_end_year INTEGER,
                image VARCHAR(1000)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS media (
                id SERIAL PRIMARY KEY,
                url VARCHAR(500) UNIQUE,
                title VARCHAR(1000),
                image VARCHAR(1000),
                category VARCHAR(100),
                date VARCHAR(100),
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
                title VARCHAR(500),
                original_title VARCHAR(500),
                description TEXT,
                full_description TEXT,
                poster VARCHAR(1000),
                year INTEGER,
                tagline TEXT,
                ru_premiere VARCHAR(100),
                world_premiere VARCHAR(100),
                content_rating VARCHAR(20),
                is_family_friendly BOOLEAN DEFAULT FALSE,
                rating_kp DECIMAL(3,1),
                kp_votes_count VARCHAR(50),
                rating_imdb DECIMAL(3,1),
                imdb_votes_count VARCHAR(50),
                user_rating DECIMAL(3,1),
                user_rating_count INTEGER DEFAULT 0,
                platform VARCHAR(200),
                number_of_episodes INTEGER
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
                title VARCHAR(500),
                year VARCHAR(10),
                genres TEXT[],
                poster TEXT,
                rating VARCHAR(10),
                UNIQUE(content_id, content_type, similar_id, similar_type)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_still (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                picture_id VARCHAR(20) NOT NULL,
                original_url TEXT NOT NULL,
                source VARCHAR(16) NOT NULL,
                UNIQUE(content_id, content_type, picture_id, source)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS content_watch_provider (
                id SERIAL PRIMARY KEY,
                content_id INTEGER NOT NULL,
                content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('film', 'series')),
                name VARCHAR(200) NOT NULL,
                url TEXT NOT NULL,
                logo TEXT NULL,
                UNIQUE(content_id, content_type, name)
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
            ('writers', 'writer'),
            ('producers', 'producer'),
            ('operators', 'operator'),
            ('composers', 'composer'),
            ('designers', 'designer'),
            ('editors', 'editor')
        ]
        
        for role_key, role_name in people_roles:
            people_list = film_data.get(role_key, [])
            if not people_list:
                continue
                
            print(f"  👥 Парсинг {role_name}s ({len(people_list)} человек) для фильма '{film_title}'")
            
            for person_data in people_list:
                person_id = person_data.get('id')
                if not person_id or person_id in self.parsed_people:
                    continue
                
                # Парсим детали участника
                person_details = self.parse_person_details(person_id)
                if person_details:
                    # Сохраняем участника в БД
                    person_db_id = self.save_person_to_db(person_details)
                    
                    # Создаем связь фильм-участник
                    self.save_content_person_relation(film_db_id, 'film', person_db_id, role_name)
                    
                    # Отмечаем как спарсенного
                    self.parsed_people.add(person_id)
                    
                    print(f"✅ {role_name}: {person_data.get('name', 'Unknown')}")
                
                # Пауза между запросами
                time.sleep(self.delays['BETWEEN_PEOPLE'])
    
    def parse_series_people(self, series_id, series_db_id, series_data):
        """Парсинг всех участников сериала"""
        series_title = series_data.get('title', 'Unknown Series')

        people_roles = [
            ('actors', 'actor'),
            ('directors', 'director'),
            ('writers', 'writer'),
            ('producers', 'producer'),
            ('operators', 'operator'),
            ('composers', 'composer'),
            ('designers', 'designer'),
            ('editors', 'editor')
        ]
        
        for role_key, role_name in people_roles:
            people_list = series_data.get(role_key, [])
            if not people_list:
                continue
                
            print(f"  👥 Парсинг {role_name}s ({len(people_list)} человек) для сериала '{series_title}'")
            
            for person_data in people_list:
                person_id = person_data.get('id')
                if not person_id or person_id in self.parsed_people:
                    continue
                
                # Парсим детали участника
                person_details = self.parse_person_details(person_id)
                if person_details:
                    # Сохраняем участника в БД
                    person_db_id = self.save_person_to_db(person_details)
                    
                    # Создаем связь сериал-участник
                    self.save_content_person_relation(series_db_id, 'series', person_db_id, role_name)
                    
                    # Отмечаем как спарсенного
                    self.parsed_people.add(person_id)
                    
                    print(f"✅ {role_name}: {person_data.get('name', 'Unknown')}")
                
                # Пауза между запросами
                time.sleep(self.delays['BETWEEN_PEOPLE'])
    
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
            INSERT INTO film (kinopoisk_id, title, original_title, description, full_description, 
                             poster, year, tagline, ru_premiere, world_premiere, content_rating, is_family_friendly,
                             duration, rating_kp, kp_votes_count, rating_imdb, imdb_votes_count,
                             budget, usa_box_office, rus_box_office, user_rating, user_rating_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (kinopoisk_id) DO UPDATE SET
                title = EXCLUDED.title,
                original_title = EXCLUDED.original_title,
                description = EXCLUDED.description,
                full_description = EXCLUDED.full_description,
                poster = EXCLUDED.poster,
                year = EXCLUDED.year,
                tagline = EXCLUDED.tagline,
                ru_premiere = EXCLUDED.ru_premiere,
                world_premiere = EXCLUDED.world_premiere,
                content_rating = EXCLUDED.content_rating,
                is_family_friendly = EXCLUDED.is_family_friendly,
                duration = EXCLUDED.duration,
                rating_kp = EXCLUDED.rating_kp,
                kp_votes_count = EXCLUDED.kp_votes_count,
                rating_imdb = EXCLUDED.rating_imdb,
                imdb_votes_count = EXCLUDED.imdb_votes_count,
                budget = EXCLUDED.budget,
                usa_box_office = EXCLUDED.usa_box_office,
                rus_box_office = EXCLUDED.rus_box_office,
                user_rating = EXCLUDED.user_rating,
                user_rating_count = EXCLUDED.user_rating_count
            RETURNING id
            """
            
            cursor.execute(insert_film, (
                film_data.get('kinopoisk_id'),
                film_data.get('title'),
                film_data.get('original_title'),
                film_data.get('description'),
                film_data.get('full_description'),
                film_data.get('poster'),
                film_data.get('year'),
                film_data.get('tagline'),
                film_data.get('ru_premiere'),
                film_data.get('world_premiere'),
                film_data.get('content_rating'),
                film_data.get('isFamilyFriendly', False),
                film_data.get('duration'),
                film_data.get('rating_kp'),
                film_data.get('kp_votes_count'),
                film_data.get('rating_imdb'),
                film_data.get('imdb_votes_count'),
                film_data.get('budget'),
                film_data.get('usa_box_office'),
                film_data.get('rus_box_office'),
                None,  # user_rating - будет обновляться автоматически
                0      # user_rating_count - будет обновляться автоматически
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
            INSERT INTO series (kinopoisk_id, title, original_title, description, full_description, 
                             poster, year, tagline, ru_premiere, world_premiere, content_rating, is_family_friendly,
                             rating_kp, kp_votes_count, rating_imdb, imdb_votes_count,
                             user_rating, user_rating_count, platform, number_of_episodes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (kinopoisk_id) DO UPDATE SET
                title = EXCLUDED.title,
                original_title = EXCLUDED.original_title,
                description = EXCLUDED.description,
                full_description = EXCLUDED.full_description,
                poster = EXCLUDED.poster,
                year = EXCLUDED.year,
                tagline = EXCLUDED.tagline,
                ru_premiere = EXCLUDED.ru_premiere,
                world_premiere = EXCLUDED.world_premiere,
                content_rating = EXCLUDED.content_rating,
                is_family_friendly = EXCLUDED.is_family_friendly,
                rating_kp = EXCLUDED.rating_kp,
                kp_votes_count = EXCLUDED.kp_votes_count,
                rating_imdb = EXCLUDED.rating_imdb,
                imdb_votes_count = EXCLUDED.imdb_votes_count,
                user_rating = EXCLUDED.user_rating,
                user_rating_count = EXCLUDED.user_rating_count,
                platform = EXCLUDED.platform,
                number_of_episodes = EXCLUDED.number_of_episodes
            RETURNING id
            """
            
            cursor.execute(insert_series, (
                series_data.get('kinopoisk_id'),
                series_data.get('title'),
                series_data.get('original_title'),
                series_data.get('description'),
                series_data.get('full_description'),
                series_data.get('poster'),
                series_data.get('year'),
                series_data.get('tagline'),
                series_data.get('ru_premiere'),
                series_data.get('world_premiere'),
                series_data.get('content_rating'),
                series_data.get('isFamilyFriendly', False),
                series_data.get('rating_kp'),
                series_data.get('kp_votes_count'),
                series_data.get('rating_imdb'),
                series_data.get('imdb_votes_count'),
                None,  # user_rating - будет обновляться автоматически
                0,     # user_rating_count - будет обновляться автоматически
                series_data.get('platform'),
                series_data.get('numberOfEpisodes')
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
                    INSERT INTO content_watch_provider (content_id, content_type, name, url, logo)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (content_id, content_type, name) DO UPDATE SET
                        url = EXCLUDED.url,
                        logo = EXCLUDED.logo
                    """,
                    (content_db_id, content_type, name, url, logo)
                )
        except Exception as e:
            print(f"❌ Ошибка сохранения провайдеров: {e}")
        finally:
            cursor.close()

    def parse_and_save_stills(self, content_kinopoisk_id: str, content_db_id: int, content_type: str):
        """Парсит кадры контента (фильма или сериала), сначала получая доступные категории, затем парсит каждую категорию."""
        try:
            main_stills_url = f"https://www.kinopoisk.ru/film/{content_kinopoisk_id}/stills/"
            self.stills_parser.load_html_from_url(main_stills_url)
            all_categories = self.stills_parser.extract_image_categories()
            
            if not all_categories:
                print(f"⚠️ Не найдено категорий кадров для {content_type} {content_kinopoisk_id}")
                return

            # Фильтруем только разрешенные категории
            allowed_types = {'stills', 'wall', 'shooting', 'screenshots'}
            filtered_categories = [cat for cat in all_categories if cat['type'] in allowed_types]
            
            if not filtered_categories:
                print(f"⚠️ Нет разрешенных категорий для {content_type} {content_kinopoisk_id}")
                return
            
            print(f"📸 Найдено категорий кадров: {len(filtered_categories)}/{len(all_categories)}")
            for category in filtered_categories:
                print(f"  - {category['name']} ({category['type']}): {category['count']} элементов")
            
            # Группируем кадры по типам
            grouped = {}
            for category in filtered_categories:
                category_type = category['type']
                category_url = f"https://www.kinopoisk.ru{category['url']}"
                
                try:
                    # Загружаем страницу конкретной категории
                    self.stills_parser.load_html_from_url(category_url)
                    # Извлекаем кадры с указанием типа
                    items = self.stills_parser.extract_stills_info(category_type)
                    grouped[category_type] = items
                    print(f"✅ Спарсено {len(items)} кадров типа '{category_type}'")
                    
                    # Пауза между категориями
                    time.sleep(self.delays['BETWEEN_FILMS'])
                except Exception as e:
                    print(f"⚠️ Не удалось спарсить категорию {category['name']} ({category_url}): {e}")
                    continue
            
            # Сохраняем все кадры в БД
            self.save_content_stills(content_db_id, content_type, grouped)
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге кадров {content_type} {content_kinopoisk_id}: {e}")

    def save_content_stills(self, content_db_id: int, content_type: str, grouped_items):
        """Сохраняет кадры контента (фильма или сериала) в таблицу content_still с указанием типа."""
        cursor = self.db_connection.cursor()
        try:
            total_saved = 0
            total_errors = 0
            
            for image_type, images in grouped_items.items():
                for image_data in images:
                    picture_id = image_data.get('id')
                    original_url = image_data.get('original')
                    
                    if not picture_id or not original_url:
                        continue
                    
                    # Используем тип изображения напрямую в поле source
                    source = image_type
                    
                    try:
                        # Начинаем новую транзакцию для каждого кадра
                        cursor.execute(
                            """
                            INSERT INTO content_still (content_id, content_type, picture_id, original_url, source)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (content_id, content_type, picture_id, source) DO UPDATE SET
                                original_url = EXCLUDED.original_url
                            """,
                            (content_db_id, content_type, picture_id, original_url, source)
                        )
                        self.db_connection.commit()
                        total_saved += 1
                        
                    except Exception as e:
                        # Откатываем неудачную транзакцию и продолжаем
                        self.db_connection.rollback()
                        print(f"⚠️ Ошибка сохранения кадра {picture_id} (тип: {source}): {e}")
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
    
    def save_person_to_db(self, person_data):
        """Сохранение участника в БД"""
        cursor = self.db_connection.cursor()
        
        try: 
            # Вставляем участника
            insert_person = """
            INSERT INTO stuff (kinopoisk_id, name, original_name, career, ganres, height, 
                               birthday_day_month, zodiac, age, birthplace, 
                               spouse, children, total_films, career_start_year, 
                               career_end_year, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (kinopoisk_id) DO UPDATE SET
                name = EXCLUDED.name,
                original_name = EXCLUDED.original_name,
                career = EXCLUDED.career,
                ganres = EXCLUDED.ganres,
                height = EXCLUDED.height,
                birthday_day_month = EXCLUDED.birthday_day_month,
                zodiac = EXCLUDED.zodiac,
                age = EXCLUDED.age,
                birthplace = EXCLUDED.birthplace,
                spouse = EXCLUDED.spouse,
                children = EXCLUDED.children,
                total_films = EXCLUDED.total_films,
                career_start_year = EXCLUDED.career_start_year,
                career_end_year = EXCLUDED.career_end_year,
                image = EXCLUDED.image
            RETURNING id
            """
            
            cursor.execute(insert_person, (
                person_data.get('kinopoisk_id'),
                person_data.get('name'),
                person_data.get('original_name'),
                person_data.get('career'),
                person_data.get('genres'),
                person_data.get('height'),
                person_data.get('birthday_day_month'),
                person_data.get('zodiac'),
                person_data.get('age'),
                person_data.get('birthplace'),
                person_data.get('spouse'),
                person_data.get('children'),
                person_data.get('total_films'),
                person_data.get('career_start_year'),
                person_data.get('career_end_year'),
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
                    title, year, genres, poster, rating
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (content_id, content_type, similar_id, similar_type) DO UPDATE SET
                    title = EXCLUDED.title,
                    year = EXCLUDED.year,
                    genres = EXCLUDED.genres,
                    poster = EXCLUDED.poster,
                    rating = EXCLUDED.rating
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
                            image = %s,
                            category = %s,
                            date = %s,
                            card_type = %s,
                            type = %s,
                            parsed_at = CURRENT_TIMESTAMP
                        WHERE url = %s
                    """, (
                        media_item.get('title'),
                        media_item.get('image'),
                        media_item.get('category'),
                        media_item.get('date'),
                        media_item.get('card_type'),
                        media_item.get('type', 'news'),
                        media_item.get('url')
                    ))
                else:
                    # Вставляем новый медиа контент
                    cursor.execute("""
                        INSERT INTO media (url, title, image, category, date, card_type, type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        media_item.get('url'),
                        media_item.get('title'),
                        media_item.get('image'),
                        media_item.get('category'),
                        media_item.get('date'),
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
