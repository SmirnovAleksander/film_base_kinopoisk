import psycopg2
import time
import requests
from bs4 import BeautifulSoup
from parser_utils.kinopoisk_parser import KinopoiskParser
from parser_utils.film_page_parser import FilmPageParser
from parser_utils.actor_page_parser import ActorPageParser
from parser_utils.stills_page_parser import StillsPageParser
from config import DATABASE_CONFIG, DELAYS, PARSING_CONFIG, LOGGING_CONFIG
from image_downloader import ImageDownloader

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
        self.actor_parser = ActorPageParser()
        self.stills_parser = StillsPageParser()
        
        # Инициализируем загрузчик изображений
        self.image_downloader = ImageDownloader()
        
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
            CREATE TABLE IF NOT EXISTS film_genre (
                id SERIAL PRIMARY KEY,
                film_id INTEGER REFERENCES film(id),
                genre_id INTEGER REFERENCES genre(id),
                UNIQUE(film_id, genre_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS film_country (
                id SERIAL PRIMARY KEY,
                film_id INTEGER REFERENCES film(id),
                country_id INTEGER REFERENCES country(id),
                UNIQUE(film_id, country_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS film_stuff (
                id SERIAL PRIMARY KEY,
                film_id INTEGER REFERENCES film(id),
                stuff_id INTEGER REFERENCES stuff(id),
                role VARCHAR(100),
                UNIQUE(film_id, stuff_id, role)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS similar_film (
                id SERIAL PRIMARY KEY,
                film_id INTEGER REFERENCES film(id),
                similar_film_id VARCHAR(20),
                similar_film_title VARCHAR(500),
                similar_film_year VARCHAR(10),
                similar_film_genres TEXT[],
                similar_film_poster TEXT,
                similar_film_rating VARCHAR(10),
                UNIQUE(film_id, similar_film_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS film_still (
                id SERIAL PRIMARY KEY,
                film_id INTEGER NOT NULL REFERENCES film(id) ON DELETE CASCADE,
                picture_id VARCHAR(20) NOT NULL,
                original_url TEXT NOT NULL,
                source VARCHAR(16) NOT NULL,
                UNIQUE(film_id, picture_id, source)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS film_watch_provider (
                id SERIAL PRIMARY KEY,
                film_id INTEGER NOT NULL REFERENCES film(id) ON DELETE CASCADE,
                name VARCHAR(200) NOT NULL,
                url TEXT NOT NULL,
                logo TEXT NULL,
                UNIQUE(film_id, name)
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
                page_url = "https://www.kinopoisk.ru/lists/movies/?b=films&b=high_rated"
            else:
                page_url = f"https://www.kinopoisk.ru/lists/movies/?b=films&b=high_rated/?page={page}"
            
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
                        self.parse_similar_films(film_details, film_db_id)

                        # Парсим кадры (stills + wall)
                        self.parse_and_save_stills(film_id, film_db_id)
                        
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
                    self.save_film_person_relation(film_db_id, person_db_id, role_name)
                    
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
    
    def parse_similar_films(self, film_data, film_db_id):
        """Парсинг похожих фильмов"""
        similar_films = film_data.get('similar_films', [])
        if not similar_films:
            return
            
        print(f"🔗 Парсинг похожих фильмов: {len(similar_films)}")
        
        for similar_film in similar_films:
            if similar_film.get('id') and similar_film.get('title'):
                self.save_similar_film_extended(film_db_id, similar_film)
    
    def save_film_to_db(self, film_data):
        """Сохранение фильма в БД"""
        cursor = self.db_connection.cursor()
        
        try:
            # # Скачиваем постер фильма
            # poster_url = film_data.get('poster')
            # if poster_url:
            #     film_id = film_data.get('kinopoisk_id')
            #     downloaded_poster = self.image_downloader.download_film_poster(poster_url, film_id)
            #     if downloaded_poster:
            #         film_data['poster'] = downloaded_poster
            #         print(f"📸 Постер фильма {film_id} скачан: {downloaded_poster}")
            #     else:
            #         print(f"⚠️ Не удалось скачать постер для фильма {film_id}")
            
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
            self.save_film_genres(film_db_id, film_data.get('genres', []))
            
            # Сохраняем страны
            self.save_film_countries(film_db_id, film_data.get('countries', []))

            # Сохраняем провайдеров просмотра
            self.save_film_watch_providers(film_db_id, film_data.get('watch_providers', []))
            
            self.db_connection.commit()
            return film_db_id
            
        except Exception as e:
            print(f"❌ Ошибка сохранения фильма: {e}")
            self.db_connection.rollback()
            return None
        finally:
            cursor.close()

    def save_film_watch_providers(self, film_db_id, providers):
        """Сохранение провайдеров просмотра фильма"""
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
                    INSERT INTO film_watch_provider (film_id, name, url, logo)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (film_id, name) DO UPDATE SET
                        url = EXCLUDED.url,
                        logo = EXCLUDED.logo
                    """,
                    (film_db_id, name, url, logo)
                )
        except Exception as e:
            print(f"❌ Ошибка сохранения провайдеров: {e}")
        finally:
            cursor.close()

    def parse_and_save_stills(self, film_kinopoisk_id: str, film_db_id: int):
        """Парсит кадры фильма, сначала получая доступные категории, затем парсит каждую категорию."""
        try:
            # Сначала парсим главную страницу кадров чтобы получить все доступные категории
            main_stills_url = f"https://www.kinopoisk.ru/film/{film_kinopoisk_id}/stills/"
            self.stills_parser.load_html_from_url(main_stills_url)
            all_categories = self.stills_parser.extract_image_categories()
            
            if not all_categories:
                print(f"⚠️ Не найдено категорий кадров для фильма {film_kinopoisk_id}")
                return
            
            # Фильтруем только разрешенные категории
            allowed_types = {'stills', 'wall', 'shooting', 'screenshots'}
            filtered_categories = [cat for cat in all_categories if cat['type'] in allowed_types]
            
            if not filtered_categories:
                print(f"⚠️ Нет разрешенных категорий для фильма {film_kinopoisk_id}")
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
            self.save_film_stills(film_db_id, grouped)
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге кадров фильма {film_kinopoisk_id}: {e}")

    def save_film_stills(self, film_db_id: int, grouped_items):
        """Сохраняет кадры фильма в таблицу film_still с указанием типа."""
        cursor = self.db_connection.cursor()
        try:
            total_saved = 0
            total_errors = 0
            
            # Удаляем ограничение БД для поля source, если оно есть
            try:
                cursor.execute("ALTER TABLE film_still DROP CONSTRAINT IF EXISTS film_still_source_check")
                self.db_connection.commit()
            except Exception as e:
                print(f"⚠️ Не удалось удалить ограничение БД: {e}")
                self.db_connection.rollback()
            
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
                            INSERT INTO film_still (film_id, picture_id, original_url, source)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (film_id, picture_id, source) DO UPDATE SET
                                original_url = EXCLUDED.original_url
                            """,
                            (film_db_id, picture_id, original_url, source)
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
            # # Скачиваем фото актера
            # photo_url = person_data.get('photo')
            # if photo_url:
            #     actor_id = person_data.get('kinopoisk_id')
            #     downloaded_photo = self.image_downloader.download_actor_photo(photo_url, actor_id)
            #     if downloaded_photo:
            #         person_data['photo'] = downloaded_photo
            #         print(f"📸 Фото актера {actor_id} скачано: {downloaded_photo}")
            #     else:
            #         print(f"⚠️ Не удалось скачать фото для актера {actor_id}")
            
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
    
    def save_film_genres(self, film_db_id, genres):
        """Сохранение жанров фильма"""
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
                
                # Создаем связь фильм-жанр
                cursor.execute(
                    "INSERT INTO film_genre (film_id, genre_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (film_db_id, genre_id)
                )
                
        except Exception as e:
            print(f"❌ Ошибка сохранения жанров: {e}")
        finally:
            cursor.close()
    
    def save_film_countries(self, film_db_id, countries):
        """Сохранение стран фильма"""
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
                
                # Создаем связь фильм-страна
                cursor.execute(
                    "INSERT INTO film_country (film_id, country_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (film_db_id, country_id)
                )
                
        except Exception as e:
            print(f"❌ Ошибка сохранения стран: {e}")
        finally:
            cursor.close()
    
    def save_film_person_relation(self, film_db_id, person_db_id, role):
        """Создание связи фильм-участник"""
        cursor = self.db_connection.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO film_stuff (film_id, stuff_id, role) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (film_db_id, person_db_id, role)
            )
        except Exception as e:
            print(f"❌ Ошибка создания связи фильм-участник: {e}")
        finally:
            cursor.close()
    
    def save_similar_film_extended(self, film_db_id, sf):
        """Сохранение похожего фильма с расширенными полями"""
        cursor = self.db_connection.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO similar_film (
                    film_id, similar_film_id, similar_film_title, similar_film_year,
                    similar_film_genres, similar_film_poster, similar_film_rating
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (film_id, similar_film_id) DO UPDATE SET
                    similar_film_title = EXCLUDED.similar_film_title,
                    similar_film_year = EXCLUDED.similar_film_year,
                    similar_film_genres = EXCLUDED.similar_film_genres,
                    similar_film_poster = EXCLUDED.similar_film_poster,
                    similar_film_rating = EXCLUDED.similar_film_rating
                """,
                (
                    film_db_id,
                    sf.get('id'),
                    sf.get('title'),
                    sf.get('year'),
                    sf.get('genres'),
                    sf.get('poster'),
                    sf.get('rating'),
                )
            )
        except Exception as e:
            print(f"❌ Ошибка создания связи похожих фильмов: {e}")
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
