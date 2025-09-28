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
    
    # Константы для настройки задержек
    DELAY_BEFORE_REQUEST = 2     # Пауза перед запросом (секунды)
    
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
            time.sleep(self.DELAY_BEFORE_REQUEST)
            
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
                    self.soup = soup  # Сохраняем в self.soup
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
        Извлекает детальную информацию о фильме из HTML элементов
        
        Returns:
            Словарь с детальной информацией о фильме
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        film_data = {}
        
        # Извлекаем данные из HTML элементов
        html_data = self._extract_from_html()
        if html_data:
            film_data.update(html_data)
        
        # Извлекаем данные из meta тегов
        meta_data = self._extract_from_meta()
        if meta_data:
            film_data.update(meta_data)
        
        return film_data
    
    def _extract_from_html(self) -> Dict:
        """Извлекает данные из HTML элементов"""
        film_data = {}
        
        # Извлекаем название фильма (data-tid="75209b22")
        title_elem = self.soup.find('span', {'data-tid': '75209b22'})
        if title_elem:
            film_data['title'] = title_elem.get_text(strip=True)
        
        # Извлекаем оригинальное название (data-tid="eb6be89")
        original_title_elem = self.soup.find('span', {'data-tid': 'eb6be89'})
        if original_title_elem:
            film_data['original_title'] = original_title_elem.get_text(strip=True)
        
        # Извлекаем описание (data-tid="bfd38da2")
        description_elem = self.soup.find('p', {'data-tid': 'bfd38da2'})
        if description_elem:
            film_data['description'] = description_elem.get_text(strip=True)
        
        # Извлекаем полное описание (data-tid="bbb11238")
        full_description_elem = self.soup.find('p', {'data-tid': 'bbb11238'})
        if full_description_elem:
            film_data['full_description'] = full_description_elem.get_text(strip=True)
        
        # Извлекаем рейтинг Кинопоиска (data-tid="939058a8")
        kp_rating_elem = self.soup.find('span', {'data-tid': '939058a8'})
        if kp_rating_elem:
            film_data['rating_kp'] = kp_rating_elem.get_text(strip=True)
        
        # Извлекаем количество оценок Кинопоиска
        kp_count_elem = self.soup.find('span', class_='styles_count__mJ4RS')
        if kp_count_elem:
            film_data['kp_votes_count'] = kp_count_elem.get_text(strip=True)
        
        # Извлекаем рейтинг IMDB (data-tid="3d4f49c8")
        imdb_rating_elem = self.soup.find('div', {'data-tid': '3d4f49c8'})
        if imdb_rating_elem:
            imdb_span = imdb_rating_elem.find('span', class_='styles_valueSection__5NAWi')
            if imdb_span:
                imdb_text = imdb_span.get_text(strip=True)
                # Извлекаем число из "IMDb: 8.50"
                imdb_match = re.search(r'(\d+\.?\d*)', imdb_text)
                if imdb_match:
                    film_data['rating_imdb'] = imdb_match.group(1)
        
        # Извлекаем количество оценок IMDB
        imdb_count_elem = self.soup.find('span', class_='styles_count__XJaJv')
        if imdb_count_elem:
            film_data['imdb_votes_count'] = imdb_count_elem.get_text(strip=True)
        
        # Извлекаем постер (data-tid="d813cf42")
        poster_elem = self.soup.find('img', {'data-tid': 'd813cf42'})
        if poster_elem and poster_elem.get('src'):
            film_data['poster'] = poster_elem.get('src')
        
        # Извлекаем год производства (data-test-id="year")
        year_elem = self.soup.find('div', {'data-test-id': 'year'})
        if year_elem:
            year_link = year_elem.find('a')
            if year_link:
                film_data['year'] = year_link.get_text(strip=True)
        
        # Извлекаем страны (data-test-id="countries")
        countries_elem = self.soup.find('div', {'data-test-id': 'countries'})
        if countries_elem:
            country_links = countries_elem.find_all('a')
            countries = [link.get_text(strip=True) for link in country_links]
            if countries:
                film_data['countries'] = countries
        
        # Извлекаем жанры (data-test-id="genres")
        genres_elem = self.soup.find('div', {'data-test-id': 'genres'})
        if genres_elem:
            genre_links = genres_elem.find_all('a')
            genres = [link.get_text(strip=True) for link in genre_links if link.get_text(strip=True) != 'слова']
            if genres:
                film_data['genres'] = genres
        
        # Извлекаем слоган (data-test-id="tagline")
        tagline_elem = self.soup.find('div', {'data-test-id': 'tagline'})
        if tagline_elem:
            tagline_div = tagline_elem.find('div', {'data-tid': 'e1e37c21'})
            if tagline_div:
                film_data['tagline'] = tagline_div.get_text(strip=True)
        
        # Извлекаем режиссеров (data-test-id="directors")
        directors_elem = self.soup.find('div', {'data-test-id': 'directors'})
        if directors_elem:
            director_links = directors_elem.find_all('a')
            directors = []
            for link in director_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    directors.append({'name': name, 'id': person_id})
            if directors:
                film_data['directors'] = directors
        
        # Извлекаем сценаристов (data-test-id="writers")
        writers_elem = self.soup.find('div', {'data-test-id': 'writers'})
        if writers_elem:
            writer_links = writers_elem.find_all('a')
            writers = []
            for link in writer_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    writers.append({'name': name, 'id': person_id})
            if writers:
                film_data['writers'] = writers
        
        # Извлекаем продюсеров (data-test-id="producers")
        producers_elem = self.soup.find('div', {'data-test-id': 'producers'})
        if producers_elem:
            producer_links = producers_elem.find_all('a')
            producers = []
            for link in producer_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    producers.append({'name': name, 'id': person_id})
            if producers:
                film_data['producers'] = producers
        
        # Извлекаем операторов (data-test-id="operators")
        operators_elem = self.soup.find('div', {'data-test-id': 'operators'})
        if operators_elem:
            operator_links = operators_elem.find_all('a')
            operators = []
            for link in operator_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    operators.append({'name': name, 'id': person_id})
            if operators:
                film_data['operators'] = operators
        
        # Извлекаем композиторов (data-test-id="composers")
        composers_elem = self.soup.find('div', {'data-test-id': 'composers'})
        if composers_elem:
            composer_links = composers_elem.find_all('a')
            composers = []
            for link in composer_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    composers.append({'name': name, 'id': person_id})
            if composers:
                film_data['composers'] = composers
        
        # Извлекаем художников (data-test-id="designers")
        designers_elem = self.soup.find('div', {'data-test-id': 'designers'})
        if designers_elem:
            designer_links = designers_elem.find_all('a')
            designers = []
            for link in designer_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    designers.append({'name': name, 'id': person_id})
            if designers:
                film_data['designers'] = designers
        
        # Извлекаем монтажеров (data-test-id="filmEditors")
        editors_elem = self.soup.find('div', {'data-test-id': 'filmEditors'})
        if editors_elem:
            editor_links = editors_elem.find_all('a')
            editors = []
            for link in editor_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    editors.append({'name': name, 'id': person_id})
            if editors:
                film_data['editors'] = editors
        
        # Извлекаем премьеру в России (data-test-id="ruPremiere")
        ru_premiere_elem = self.soup.find('div', {'data-test-id': 'ruPremiere'})
        if ru_premiere_elem:
            premiere_link = ru_premiere_elem.find('a')
            if premiere_link:
                film_data['ru_premiere'] = premiere_link.get_text(strip=True)
        
        # Извлекаем премьеру в мире (data-test-id="worldPremieres")
        world_premiere_elem = self.soup.find('div', {'data-test-id': 'worldPremieres'})
        if world_premiere_elem:
            premiere_link = world_premiere_elem.find('a')
            if premiere_link:
                film_data['world_premiere'] = premiere_link.get_text(strip=True)
        
        # Извлекаем возрастной рейтинг (data-test-id="ageRestriction")
        age_elem = self.soup.find('div', {'data-test-id': 'ageRestriction'})
        if age_elem:
            age_span = age_elem.find('span', {'data-tid': '5c1ffa33'})
            if age_span:
                film_data['age_rating'] = age_span.get_text(strip=True)
        
        # Извлекаем продолжительность (data-test-id="duration")
        duration_elem = self.soup.find('div', {'data-test-id': 'duration'})
        if duration_elem:
            duration_div = duration_elem.find('div', {'data-tid': 'e1e37c21'})
            if duration_div:
                film_data['duration'] = duration_div.get_text(strip=True)
        
        # Извлекаем похожие фильмы (data-tid="36b81cbf")
        similar_films_elem = self.soup.find('div', {'data-tid': '36b81cbf'})
        if similar_films_elem:
            similar_films = []
            # Находим все элементы карусели по data-tid="67feb64f"
            carousel_items = similar_films_elem.find_all('div', {'data-tid': '67feb64f'})
            for item in carousel_items:
                # Извлекаем ссылку на фильм
                film_link = item.find('a', {'data-test-id': 'next-link'})
                if film_link and film_link.get('href'):
                    # Извлекаем ID из URL /film/5919/ -> 5919
                    film_id = film_link.get('href').split('/film/')[1].rstrip('/')
                    
                    # Извлекаем название фильма
                    title_span = item.find('span', {'data-tid': 'ecca3393'})
                    if title_span:
                        title = title_span.get_text(strip=True)
                        similar_films.append({'title': title, 'id': film_id})
            
            if similar_films:
                film_data['similar_films'] = similar_films
        
        # Извлекаем актеров в главных ролях (data-tid="38ecf27e")
        actors_elem = self.soup.find('div', {'data-tid': '38ecf27e'})
        if actors_elem:
            actors = []
            # Находим все ссылки на актеров
            actor_links = actors_elem.find_all('a', {'data-test-id': 'next-link'})
            for link in actor_links:
                if link.get('href') and '/name/' in link.get('href'):
                    name = link.get_text(strip=True)
                    person_id = link.get('href').split('/name/')[1].rstrip('/')
                    actors.append({'name': name, 'id': person_id})
            
            if actors:
                film_data['actors'] = actors
        
        return film_data
    
    def _extract_from_meta(self) -> Dict:
        """Извлекает данные из meta тегов"""
        # TODO: Добавить парсинг meta тегов
        return {}
    
    def save_to_json(self, film_data: Dict, output_file: str = 'output/film_details.json'):
        """
        Сохраняет данные о фильме в JSON файл (ОТКЛЮЧЕНО)
        
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
            actor_names = [actor['name'] for actor in actors if isinstance(actor, dict)]
            print(f"👥 Актеры: {', '.join(actor_names)}")
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
