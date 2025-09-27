#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для страницы отдельного фильма на Кинопоиске
Извлекает детальную информацию о фильме
"""

import json
import os
import re
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import requests


class FilmPageParser:
    """Парсер для страницы отдельного фильма"""
    
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
    
    def extract_film_details(self) -> Dict:
        """
        Извлекает детальную информацию о фильме
        
        Returns:
            Словарь с детальной информацией о фильме
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        film_data = {}
        
        # Извлекаем данные из JSON
        json_data = self._extract_from_json()
        if json_data:
            film_data.update(json_data)
        
        # Извлекаем данные из HTML элементов
        html_data = self._extract_from_html()
        if html_data:
            film_data.update(html_data)
        
        # Извлекаем данные из meta тегов
        meta_data = self._extract_from_meta()
        if meta_data:
            film_data.update(meta_data)
        
        return film_data
    
    def _extract_from_json(self) -> Dict:
        """Извлекает данные из JSON в script тегах"""
        film_data = {}
        
        # Поиск script тегов с JSON данными
        script_tags = self.soup.find_all('script', type='application/json')
        
        for script in script_tags:
            try:
                json_data = json.loads(script.string)
                film_info = self._find_film_in_json(json_data)
                if film_info:
                    film_data.update(film_info)
            except (json.JSONDecodeError, AttributeError):
                continue
        
        return film_data
    
    def _find_film_in_json(self, data: Dict, path: str = "") -> Dict:
        """Рекурсивно ищет данные о фильме в JSON структуре"""
        film_info = {}
        
        if isinstance(data, dict):
            # Проверяем, является ли текущий объект фильмом
            if self._is_film_object(data):
                film_info = self._extract_film_data(data)
            
            # Рекурсивно ищем в значениях словаря
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    result = self._find_film_in_json(value, f"{path}.{key}" if path else key)
                    if result:
                        film_info.update(result)
                        
        elif isinstance(data, list):
            # Рекурсивно ищем в элементах списка
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    result = self._find_film_in_json(item, f"{path}[{i}]" if path else f"[{i}]")
                    if result:
                        film_info.update(result)
        
        return film_info
    
    def _is_film_object(self, obj: Dict) -> bool:
        """Проверяет, является ли объект данными о фильме"""
        film_indicators = [
            'name', 'title', 'ruName', 'enName', 'originalName',
            'year', 'rating', 'imdbRating', 'kpRating', 'kinopoisk',
            'genre', 'genres', 'country', 'countries',
            'director', 'actors', 'description', 'poster',
            'duration', 'id', 'filmId', 'kinopoiskId'
        ]
        
        found_indicators = sum(1 for indicator in film_indicators if indicator in obj)
        has_typename = '__typename' in obj and obj['__typename'] in ['Film', 'Movie', 'Title']
        
        return found_indicators >= 3 or has_typename
    
    def _extract_film_data(self, film_obj: Dict) -> Dict:
        """Извлекает структурированные данные о фильме"""
        film_data = {
            'title': self._extract_title(film_obj),
            'original_title': self._extract_original_title(film_obj),
            'year': self._extract_year(film_obj),
            'rating': self._extract_rating(film_obj),
            'imdb_rating': self._extract_imdb_rating(film_obj),
            'genres': self._extract_genres(film_obj),
            'countries': self._extract_countries(film_obj),
            'director': self._extract_director(film_obj),
            'actors': self._extract_actors(film_obj),
            'description': self._extract_description(film_obj),
            'poster': self._extract_poster(film_obj),
            'duration': self._extract_duration(film_obj),
            'age_rating': self._extract_age_rating(film_obj),
            'id': self._extract_id(film_obj),
            'budget': self._extract_budget(film_obj),
            'box_office': self._extract_box_office(film_obj),
            'premiere': self._extract_premiere(film_obj),
            'studio': self._extract_studio(film_obj)
        }
        
        # Очищаем пустые значения
        return {k: v for k, v in film_data.items() if v is not None and v != ''}
    
    def _extract_title(self, film_obj: Dict) -> Optional[str]:
        """Извлекает название фильма"""
        title_fields = ['name', 'title', 'ruName', 'enName', 'originalName']
        
        for field in title_fields:
            if field in film_obj:
                title_data = film_obj[field]
                
                if isinstance(title_data, str):
                    return title_data
                
                if isinstance(title_data, dict):
                    if 'russian' in title_data and title_data['russian']:
                        return title_data['russian']
                    elif 'original' in title_data and title_data['original']:
                        return title_data['original']
                    elif 'name' in title_data and title_data['name']:
                        return title_data['name']
        
        return None
    
    def _extract_original_title(self, film_obj: Dict) -> Optional[str]:
        """Извлекает оригинальное название"""
        title_fields = ['originalName', 'enName', 'original']
        
        for field in title_fields:
            if field in film_obj:
                title_data = film_obj[field]
                
                if isinstance(title_data, str):
                    return title_data
                
                if isinstance(title_data, dict):
                    if 'original' in title_data and title_data['original']:
                        return title_data['original']
                    elif 'english' in title_data and title_data['english']:
                        return title_data['english']
        
        return None
    
    def _extract_year(self, film_obj: Dict) -> Optional[str]:
        """Извлекает год выпуска"""
        year_fields = ['year', 'releaseYear', 'productionYear']
        
        for field in year_fields:
            if field in film_obj and film_obj[field]:
                year = str(film_obj[field])
                if year.isdigit() and 1900 <= int(year) <= 2030:
                    return year
        
        return None
    
    def _extract_rating(self, film_obj: Dict) -> Optional[str]:
        """Извлекает рейтинг Кинопоиска"""
        rating_fields = ['rating', 'kpRating', 'kinopoisk']
        
        for field in rating_fields:
            if field in film_obj and film_obj[field]:
                rating_data = film_obj[field]
                
                if isinstance(rating_data, (int, float)):
                    return str(rating_data)
                
                if isinstance(rating_data, str):
                    match = re.search(r'\d+\.?\d*', rating_data)
                    if match:
                        return match.group()
                
                if isinstance(rating_data, dict) and 'value' in rating_data:
                    return str(rating_data['value'])
        
        return None
    
    def _extract_imdb_rating(self, film_obj: Dict) -> Optional[str]:
        """Извлекает рейтинг IMDB"""
        imdb_fields = ['imdbRating', 'imdb']
        
        for field in imdb_fields:
            if field in film_obj and film_obj[field]:
                rating_data = film_obj[field]
                
                if isinstance(rating_data, (int, float)):
                    return str(rating_data)
                
                if isinstance(rating_data, str):
                    match = re.search(r'\d+\.?\d*', rating_data)
                    if match:
                        return match.group()
                
                if isinstance(rating_data, dict) and 'value' in rating_data:
                    return str(rating_data['value'])
        
        return None
    
    def _extract_genres(self, film_obj: Dict) -> Optional[List[str]]:
        """Извлекает жанры фильма"""
        genre_fields = ['genre', 'genres', 'genreNames']
        
        for field in genre_fields:
            if field in film_obj and film_obj[field]:
                genres_data = film_obj[field]
                
                if isinstance(genres_data, list):
                    genres = []
                    for item in genres_data:
                        if isinstance(item, str):
                            genres.append(item)
                        elif isinstance(item, dict):
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
                
                if isinstance(countries_data, list):
                    countries = []
                    for item in countries_data:
                        if isinstance(item, str):
                            countries.append(item)
                        elif isinstance(item, dict):
                            name = item.get('name') or item.get('title') or item.get('russian')
                            if name:
                                countries.append(name)
                    if countries:
                        return countries
        
        return None
    
    def _extract_director(self, film_obj: Dict) -> Optional[str]:
        """Извлекает режиссера"""
        director_fields = ['director', 'directors']
        
        for field in director_fields:
            if field in film_obj and film_obj[field]:
                director_data = film_obj[field]
                
                if isinstance(director_data, str):
                    return director_data
                
                if isinstance(director_data, list) and director_data:
                    return director_data[0]
                
                if isinstance(director_data, dict):
                    name = director_data.get('name') or director_data.get('title')
                    if name:
                        return name
        
        return None
    
    def _extract_actors(self, film_obj: Dict) -> Optional[List[str]]:
        """Извлекает актеров"""
        actor_fields = ['actors', 'cast', 'stars']
        
        for field in actor_fields:
            if field in film_obj and film_obj[field]:
                actors_data = film_obj[field]
                
                if isinstance(actors_data, list):
                    actors = []
                    for item in actors_data:
                        if isinstance(item, str):
                            actors.append(item)
                        elif isinstance(item, dict):
                            name = item.get('name') or item.get('title')
                            if name:
                                actors.append(name)
                    if actors:
                        return actors
        
        return None
    
    def _extract_description(self, film_obj: Dict) -> Optional[str]:
        """Извлекает описание фильма"""
        desc_fields = ['description', 'plot', 'synopsis', 'storyline']
        
        for field in desc_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_poster(self, film_obj: Dict) -> Optional[str]:
        """Извлекает постер"""
        poster_fields = ['poster', 'posterUrl', 'image', 'cover']
        
        for field in poster_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_duration(self, film_obj: Dict) -> Optional[str]:
        """Извлекает продолжительность"""
        duration_fields = ['duration', 'runtime', 'length']
        
        for field in duration_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_age_rating(self, film_obj: Dict) -> Optional[str]:
        """Извлекает возрастной рейтинг"""
        age_fields = ['ageRating', 'mpaaRating', 'certification', 'age']
        
        for field in age_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_id(self, film_obj: Dict) -> Optional[str]:
        """Извлекает ID фильма"""
        id_fields = ['id', 'filmId', 'kinopoiskId', 'kpId']
        
        for field in id_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_budget(self, film_obj: Dict) -> Optional[str]:
        """Извлекает бюджет"""
        budget_fields = ['budget', 'productionBudget']
        
        for field in budget_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_box_office(self, film_obj: Dict) -> Optional[str]:
        """Извлекает кассовые сборы"""
        box_fields = ['boxOffice', 'worldwideGross', 'gross']
        
        for field in box_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_premiere(self, film_obj: Dict) -> Optional[str]:
        """Извлекает дату премьеры"""
        premiere_fields = ['premiere', 'releaseDate', 'premiereDate']
        
        for field in premiere_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_studio(self, film_obj: Dict) -> Optional[str]:
        """Извлекает студию"""
        studio_fields = ['studio', 'productionCompany', 'company']
        
        for field in studio_fields:
            if field in film_obj and film_obj[field]:
                return str(film_obj[field])
        
        return None
    
    def _extract_from_html(self) -> Dict:
        """Извлекает данные из HTML элементов"""
        film_data = {}
        
        # Извлекаем название из title
        title_tag = self.soup.find('title')
        if title_tag:
            title_text = title_tag.get_text()
            # Парсим название из title
            match = re.search(r'«([^»]+)»', title_text)
            if match:
                film_data['title'] = match.group(1)
        
        # Извлекаем описание из meta description
        desc_meta = self.soup.find('meta', attrs={'name': 'description'})
        if desc_meta and desc_meta.get('content'):
            film_data['description'] = desc_meta.get('content')
        
        # Извлекаем постер из og:image
        poster_meta = self.soup.find('meta', attrs={'property': 'og:image'})
        if poster_meta and poster_meta.get('content'):
            film_data['poster'] = poster_meta.get('content')
        
        return film_data
    
    def _extract_from_meta(self) -> Dict:
        """Извлекает данные из meta тегов"""
        film_data = {}
        
        # Извлекаем различные данные из meta тегов
        meta_tags = {
            'og:title': 'title',
            'og:description': 'description',
            'og:image': 'poster',
            'og:url': 'url'
        }
        
        for meta_prop, field_name in meta_tags.items():
            meta_tag = self.soup.find('meta', attrs={'property': meta_prop})
            if meta_tag and meta_tag.get('content'):
                film_data[field_name] = meta_tag.get('content')
        
        return film_data
    
    def save_to_json(self, film_data: Dict, output_file: str = 'output/film_details.json'):
        """
        Сохраняет данные о фильме в JSON файл
        
        Args:
            film_data: Данные о фильме для сохранения
            output_file: Путь к выходному файлу
        """
        try:
            # Создаем папку output если её нет
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(film_data, file, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в файл: {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    
    def print_film_details(self, film_data: Dict):
        """
        Выводит детальную информацию о фильме
        
        Args:
            film_data: Данные о фильме
        """
        print("\n=== Детальная информация о фильме ===")
        print("-" * 50)
        
        # Основная информация
        if film_data.get('title'):
            print(f"🎬 Название: {film_data['title']}")
        
        if film_data.get('original_title'):
            print(f"🌍 Оригинальное название: {film_data['original_title']}")
        
        if film_data.get('year'):
            print(f"📅 Год: {film_data['year']}")
        
        if film_data.get('rating'):
            print(f"⭐ Рейтинг Кинопоиска: {film_data['rating']}")
        
        if film_data.get('imdb_rating'):
            print(f"🎯 Рейтинг IMDB: {film_data['imdb_rating']}")
        
        # Жанры и страны
        if film_data.get('genres'):
            print(f"🎭 Жанры: {', '.join(film_data['genres'])}")
        
        if film_data.get('countries'):
            print(f"🌎 Страны: {', '.join(film_data['countries'])}")
        
        # Создатели
        if film_data.get('director'):
            print(f"🎬 Режиссер: {film_data['director']}")
        
        if film_data.get('actors'):
            actors = film_data['actors'][:5]  # Показываем первых 5 актеров
            print(f"👥 Актеры: {', '.join(actors)}")
            if len(film_data['actors']) > 5:
                print(f"    ... и еще {len(film_data['actors']) - 5}")
        
        # Дополнительная информация
        if film_data.get('duration'):
            print(f"⏱️ Продолжительность: {film_data['duration']} мин")
        
        if film_data.get('age_rating'):
            print(f"🔞 Возрастной рейтинг: {film_data['age_rating']}")
        
        if film_data.get('budget'):
            print(f"💰 Бюджет: {film_data['budget']}")
        
        if film_data.get('box_office'):
            print(f"💵 Кассовые сборы: {film_data['box_office']}")
        
        if film_data.get('premiere'):
            print(f"🎪 Премьера: {film_data['premiere']}")
        
        if film_data.get('studio'):
            print(f"🏢 Студия: {film_data['studio']}")
        
        # Описание
        if film_data.get('description'):
            desc = film_data['description']
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"\n📝 Описание: {desc}")
        
        print()


def main():
    """Основная функция для демонстрации работы парсера"""
    parser = FilmPageParser()
    
    try:
        # Загружаем HTML из файла
        print("Загружаем HTML файл...")
        parser.load_html_from_file('templates/film_page_kinopoisk.html')
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию о фильме...")
        film_data = parser.extract_film_details()
        
        # Выводим результаты
        parser.print_film_details(film_data)
        
        # Сохраняем в JSON
        parser.save_to_json(film_data, 'output/film_details.json')
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
