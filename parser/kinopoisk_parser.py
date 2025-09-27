#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для извлечения данных о фильмах с Кинопоиска
Использует BeautifulSoup4 и lxml для парсинга HTML
"""

import json
import os
import re
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import requests


class KinopoiskParser:
    """Парсер для извлечения данных о фильмах с Кинопоиска"""
    
    def __init__(self, html_file_path: str = None):
        """
        Инициализация парсера
        
        Args:
            html_file_path: Путь к HTML файлу для парсинга
        """
        self.html_file_path = html_file_path
        self.soup = None
        
    def load_html_from_file(self, file_path: str = None) -> BeautifulSoup:
        """
        Загружает HTML из файла
        
        Args:
            file_path: Путь к HTML файлу
            
        Returns:
            BeautifulSoup объект
        """
        if file_path:
            self.html_file_path = file_path
            
        if not self.html_file_path:
            raise ValueError("Не указан путь к HTML файлу")
            
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                
            self.soup = BeautifulSoup(html_content, 'lxml')
            return self.soup
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.html_file_path} не найден")
        except Exception as e:
            raise Exception(f"Ошибка при загрузке HTML файла: {e}")
    
    def load_html_from_url(self, url: str) -> BeautifulSoup:
        """
        Загружает HTML с веб-страницы Кинопоиска
        
        Args:
            url: URL страницы для парсинга
            
        Returns:
            BeautifulSoup объект
        """
        try:
            # Расширенные заголовки для обхода защиты от ботов
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'Referer': 'https://www.kinopoisk.ru/'
            }
            
            # Настройки сессии для обхода защиты
            session = requests.Session()
            session.headers.update(headers)
            
            # Загружаем cookies если есть
            self._load_cookies(session)
            
            # Делаем запрос с задержкой
            import time
            time.sleep(2)
            
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            # Проверяем, не попали ли на страницу с капчей
            if 'SmartCaptcha' in response.text or 'робот' in response.text.lower():
                print("⚠️ Обнаружена защита от ботов. Попробуем обойти...")
                return self._handle_captcha(session, url)
            
            self.soup = BeautifulSoup(response.content, 'lxml')
            return self.soup
            
        except Exception as e:
            raise Exception(f"Ошибка при загрузке HTML с URL: {e}")
    
    def _load_cookies(self, session: requests.Session):
        """Загружает cookies из файла если он существует"""
        try:
            cookies_file = 'parser/cookies/session.json'
            if os.path.exists(cookies_file):
                with open(cookies_file, 'r', encoding='utf-8') as f:
                    cookies_data = json.load(f)
                    
                    # Обрабатываем разные форматы cookies
                    if 'cookies' in cookies_data:
                        # Формат: {"cookies": {"name": "value"}}
                        for name, value in cookies_data['cookies'].items():
                            session.cookies.set(name, value, domain='.kinopoisk.ru')
                    elif isinstance(cookies_data, list):
                        # Формат: [{"name": "name", "value": "value"}]
                        for cookie in cookies_data:
                            session.cookies.set(
                                cookie['name'], 
                                cookie['value'], 
                                domain=cookie.get('domain', '.kinopoisk.ru')
                            )
                    
                print("✓ Cookies загружены")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить cookies: {e}")
    
    def _handle_captcha(self, session: requests.Session, url: str) -> BeautifulSoup:
        """Обрабатывает страницу с капчей"""
        print("🔄 Пытаемся обойти защиту...")
        
        # Дополнительные заголовки для обхода
        session.headers.update({
            'X-Requested-With': 'XMLHttpRequest',
            'X-Forwarded-For': '127.0.0.1',
            'X-Real-IP': '127.0.0.1'
        })
        
        # Пробуем разные подходы
        approaches = [
            lambda: self._try_mobile_headers(session, url),
            lambda: self._try_different_user_agent(session, url),
            lambda: self._try_with_referer(session, url)
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"🔄 Попытка {i}/3...")
                soup = approach()
                if soup and 'SmartCaptcha' not in str(soup):
                    print("✓ Защита обойдена!")
                    return soup
            except Exception as e:
                print(f"❌ Попытка {i} не удалась: {e}")
                continue
        
        raise Exception("Не удалось обойти защиту от ботов. Попробуйте позже или используйте локальный HTML файл.")
    
    def _try_mobile_headers(self, session: requests.Session, url: str) -> BeautifulSoup:
        """Пробует мобильные заголовки"""
        mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
        }
        session.headers.update(mobile_headers)
        
        response = session.get(url, timeout=30)
        return BeautifulSoup(response.content, 'lxml')
    
    def _try_different_user_agent(self, session: requests.Session, url: str) -> BeautifulSoup:
        """Пробует другой User-Agent"""
        new_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        session.headers.update(new_headers)
        
        response = session.get(url, timeout=30)
        return BeautifulSoup(response.content, 'lxml')
    
    def _try_with_referer(self, session: requests.Session, url: str) -> BeautifulSoup:
        """Пробует с реферером"""
        session.headers.update({
            'Referer': 'https://www.google.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        response = session.get(url, timeout=30)
        return BeautifulSoup(response.content, 'lxml')
    
    def extract_films_from_json_data(self) -> List[Dict]:
        """
        Извлекает данные о фильмах из JSON данных в script тегах
        
        Returns:
            Список словарей с данными о фильмах
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        films = []
        
        # Поиск script тегов с JSON данными
        script_tags = self.soup.find_all('script', type='application/json')
        
        for script in script_tags:
            try:
                # Парсим JSON данные
                json_data = json.loads(script.string)
                
                # Ищем данные о фильмах в различных структурах
                films_data = self._find_films_in_json(json_data)
                if films_data:
                    films.extend(films_data)
                    
            except (json.JSONDecodeError, AttributeError):
                continue
        
        # Также ищем в обычных script тегах
        all_scripts = self.soup.find_all('script')
        for script in all_scripts:
            if script.string and ('film' in script.string.lower() or 'movie' in script.string.lower()):
                try:
                    # Попытка найти JSON в тексте скрипта
                    json_match = re.search(r'\{.*\}', script.string, re.DOTALL)
                    if json_match:
                        json_data = json.loads(json_match.group())
                        films_data = self._find_films_in_json(json_data)
                        if films_data:
                            films.extend(films_data)
                except (json.JSONDecodeError, AttributeError):
                    continue
        
        return films
    
    def _find_films_in_json(self, data: Dict, path: str = "") -> List[Dict]:
        """
        Рекурсивно ищет данные о фильмах в JSON структуре
        
        Args:
            data: JSON данные для поиска
            path: Текущий путь в JSON структуре
            
        Returns:
            Список найденных фильмов
        """
        films = []
        
        if isinstance(data, dict):
            # Проверяем, является ли текущий объект фильмом
            if self._is_film_object(data):
                films.append(self._extract_film_data(data))
            
            # Рекурсивно ищем в значениях словаря
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    films.extend(self._find_films_in_json(value, f"{path}.{key}" if path else key))
                    
        elif isinstance(data, list):
            # Рекурсивно ищем в элементах списка
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    films.extend(self._find_films_in_json(item, f"{path}[{i}]" if path else f"[{i}]"))
        
        return films
    
    def _is_film_object(self, obj: Dict) -> bool:
        """
        Проверяет, является ли объект данными о фильме
        
        Args:
            obj: Объект для проверки
            
        Returns:
            True, если объект содержит данные о фильме
        """
        # Ключевые поля, которые могут указывать на фильм
        film_indicators = [
            'name', 'title', 'ruName', 'enName', 'originalName',
            'year', 'rating', 'imdbRating', 'kpRating', 'kinopoisk',
            'genre', 'genres', 'country', 'countries',
            'director', 'actors', 'description', 'poster',
            'duration', 'id', 'filmId', 'kinopoiskId'
        ]
        
        # Проверяем наличие хотя бы нескольких ключевых полей
        found_indicators = sum(1 for indicator in film_indicators if indicator in obj)
        
        # Дополнительная проверка на наличие __typename
        has_typename = '__typename' in obj and obj['__typename'] in ['Film', 'Movie', 'Title']
        
        return found_indicators >= 3 or has_typename
    
    def _extract_film_data(self, film_obj: Dict) -> Dict:
        """
        Извлекает структурированные данные о фильме
        
        Args:
            film_obj: Объект с данными о фильме
            
        Returns:
            Словарь с извлеченными данными о фильме
        """
        film_data = {
            'title': self._extract_title(film_obj),
            'year': self._extract_year(film_obj),
            'rating': self._extract_rating(film_obj),
            'genres': self._extract_genres(film_obj),
            'countries': self._extract_countries(film_obj),
            'director': self._get_value(film_obj, ['director', 'directors']),
            'actors': self._get_list_value(film_obj, ['actors', 'cast']),
            'description': self._get_value(film_obj, ['description', 'plot', 'synopsis']),
            'poster': self._get_value(film_obj, ['poster', 'posterUrl', 'image']),
            'duration': self._get_value(film_obj, ['duration', 'runtime', 'length']),
            'age_rating': self._get_value(film_obj, ['ageRating', 'mpaaRating', 'certification']),
            'id': self._get_value(film_obj, ['id', 'filmId', 'kinopoiskId'])
        }
        
        # Очищаем пустые значения
        return {k: v for k, v in film_data.items() if v is not None and v != ''}
    
    def _get_value(self, obj: Dict, keys: List[str]) -> Optional[str]:
        """
        Получает значение по одному из возможных ключей
        
        Args:
            obj: Словарь для поиска
            keys: Список возможных ключей
            
        Returns:
            Найденное значение или None
        """
        for key in keys:
            if key in obj and obj[key] is not None:
                return str(obj[key])
        return None
    
    def _get_list_value(self, obj: Dict, keys: List[str]) -> Optional[List[str]]:
        """
        Получает список значений по одному из возможных ключей
        
        Args:
            obj: Словарь для поиска
            keys: Список возможных ключей
            
        Returns:
            Найденный список или None
        """
        for key in keys:
            if key in obj and obj[key] is not None:
                value = obj[key]
                if isinstance(value, list):
                    return [str(item) for item in value if item is not None]
                elif isinstance(value, str):
                    return [value]
        return None
    
    def _extract_title(self, film_obj: Dict) -> Optional[str]:
        """Извлекает название фильма из различных структур"""
        # Пробуем разные варианты структуры title
        title_fields = ['name', 'title', 'ruName', 'enName', 'originalName']
        
        for field in title_fields:
            if field in film_obj:
                title_data = film_obj[field]
                
                # Если это строка
                if isinstance(title_data, str):
                    return title_data
                
                # Если это словарь с полями russian/original
                if isinstance(title_data, dict):
                    if 'russian' in title_data and title_data['russian']:
                        return title_data['russian']
                    elif 'original' in title_data and title_data['original']:
                        return title_data['original']
                    elif 'name' in title_data and title_data['name']:
                        return title_data['name']
        
        return None
    
    def _extract_year(self, film_obj: Dict) -> Optional[str]:
        """Извлекает год выпуска"""
        year_fields = ['year', 'releaseYear', 'productionYear']
        
        for field in year_fields:
            if field in film_obj and film_obj[field]:
                year = str(film_obj[field])
                # Проверяем, что это валидный год
                if year.isdigit() and 1900 <= int(year) <= 2030:
                    return year
        
        return None
    
    def _extract_rating(self, film_obj: Dict) -> Optional[str]:
        """Извлекает рейтинг фильма"""
        rating_fields = ['rating', 'kpRating', 'imdbRating', 'kinopoisk']
        
        for field in rating_fields:
            if field in film_obj and film_obj[field]:
                rating_data = film_obj[field]
                
                # Если это число
                if isinstance(rating_data, (int, float)):
                    return str(rating_data)
                
                # Если это строка
                if isinstance(rating_data, str):
                    # Извлекаем число из строки
                    import re
                    match = re.search(r'\d+\.?\d*', rating_data)
                    if match:
                        return match.group()
                
                # Если это словарь с полем value
                if isinstance(rating_data, dict) and 'value' in rating_data:
                    return str(rating_data['value'])
        
        return None
    
    def _extract_genres(self, film_obj: Dict) -> Optional[List[str]]:
        """Извлекает жанры фильма"""
        genre_fields = ['genre', 'genres', 'genreNames']
        
        for field in genre_fields:
            if field in film_obj and film_obj[field]:
                genres_data = film_obj[field]
                
                # Если это список
                if isinstance(genres_data, list):
                    genres = []
                    for item in genres_data:
                        if isinstance(item, str):
                            genres.append(item)
                        elif isinstance(item, dict):
                            # Ищем название жанра в словаре
                            name = item.get('name') or item.get('title') or item.get('russian')
                            if name:
                                genres.append(name)
                    if genres:
                        return genres
        
        return None
    
    def _extract_countries(self, film_obj: Dict) -> Optional[List[str]]:
        """Извлекает страны производства"""
        country_fields = ['country', 'countries', 'countryNames']
        
        for field in country_fields:
            if field in film_obj and film_obj[field]:
                countries_data = film_obj[field]
                
                # Если это список
                if isinstance(countries_data, list):
                    countries = []
                    for item in countries_data:
                        if isinstance(item, str):
                            countries.append(item)
                        elif isinstance(item, dict):
                            # Ищем название страны в словаре
                            name = item.get('name') or item.get('title') or item.get('russian')
                            if name:
                                countries.append(name)
                    if countries:
                        return countries
        
        return None
    
    def extract_films_from_html_elements(self) -> List[Dict]:
        """
        Извлекает данные о фильмах из HTML элементов
        
        Returns:
            Список словарей с данными о фильмах
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        films = []
        
        # Поиск различных HTML элементов, которые могут содержать данные о фильмах
        selectors = [
            '[data-tid*="film"]',
            '[data-tid*="movie"]',
            '.film-item',
            '.movie-item',
            '.film-card',
            '.movie-card',
            '[class*="film"]',
            '[class*="movie"]'
        ]
        
        for selector in selectors:
            elements = self.soup.select(selector)
            for element in elements:
                film_data = self._extract_film_from_element(element)
                if film_data:
                    films.append(film_data)
        
        return films
    
    def _extract_film_from_element(self, element) -> Optional[Dict]:
        """
        Извлекает данные о фильме из HTML элемента
        
        Args:
            element: BeautifulSoup элемент
            
        Returns:
            Словарь с данными о фильме или None
        """
        film_data = {}
        
        # Поиск названия фильма
        title_selectors = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            '.title', '.name', '.film-title', '.movie-title',
            '[data-tid*="title"]', '[data-tid*="name"]'
        ]
        
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem and title_elem.get_text(strip=True):
                film_data['title'] = title_elem.get_text(strip=True)
                break
        
        # Поиск года
        year_text = element.get_text()
        year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
        if year_match:
            film_data['year'] = year_match.group()
        
        # Поиск рейтинга
        rating_selectors = [
            '.rating', '.score', '.rate',
            '[data-tid*="rating"]', '[data-tid*="score"]'
        ]
        
        for selector in rating_selectors:
            rating_elem = element.select_one(selector)
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'\d+\.?\d*', rating_text)
                if rating_match:
                    film_data['rating'] = rating_match.group()
                    break
        
        # Поиск жанров
        genre_elem = element.select_one('.genre, .genres, [data-tid*="genre"]')
        if genre_elem:
            film_data['genres'] = [genre.strip() for genre in genre_elem.get_text().split(',')]
        
        # Поиск постеров
        poster_elem = element.select_one('img')
        if poster_elem and poster_elem.get('src'):
            film_data['poster'] = poster_elem.get('src')
        
        return film_data if film_data else None
    
    def parse_all_films(self) -> List[Dict]:
        """
        Парсит все доступные данные о фильмах
        
        Returns:
            Список всех найденных фильмов
        """
        all_films = []
        
        # Извлекаем из JSON данных
        json_films = self.extract_films_from_json_data()
        all_films.extend(json_films)
        
        # Извлекаем из HTML элементов
        html_films = self.extract_films_from_html_elements()
        all_films.extend(html_films)
        
        # Удаляем дубликаты по названию и году
        unique_films = []
        seen = set()
        
        for film in all_films:
            key = (film.get('title', ''), film.get('year', ''))
            if key not in seen and film.get('title'):
                seen.add(key)
                unique_films.append(film)
        
        return unique_films
    
    def save_to_json(self, films: List[Dict], output_file: str = 'output/films_data.json'):
        """
        Сохраняет данные о фильмах в JSON файл
        
        Args:
            films: Список фильмов для сохранения
            output_file: Путь к выходному файлу
        """
        try:
            # Создаем папку output если её нет
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(films, file, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в файл: {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    
    def print_films_summary(self, films: List[Dict]):
        """
        Выводит краткую сводку по найденным фильмам
        
        Args:
            films: Список фильмов
        """
        print(f"\nНайдено фильмов: {len(films)}")
        print("-" * 50)
        
        for i, film in enumerate(films[:10], 1):  # Показываем первые 10
            title = film.get('title', 'Неизвестно')
            year = film.get('year', 'Неизвестно')
            rating = film.get('rating', 'Неизвестно')
            genres = film.get('genres', [])
            
            print(f"{i}. {title} ({year})")
            print(f"   Рейтинг: {rating}")
            if genres:
                print(f"   Жанры: {', '.join(genres)}")
            print()


def main():
    """Основная функция для демонстрации работы парсера"""
    # Создаем экземпляр парсера
    parser = KinopoiskParser()
    
    try:
        # Загружаем HTML из файла
        print("Загружаем HTML файл...")
        parser.load_html_from_file('templates/all_films_kinopoisk.html')
        
        # Парсим все фильмы
        print("Парсим данные о фильмах...")
        films = parser.parse_all_films()
        
        # Выводим сводку
        parser.print_films_summary(films)
        
        # Сохраняем в JSON
        parser.save_to_json(films, 'parsed_films.json')
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
