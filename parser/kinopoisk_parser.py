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
    
    # Константы для настройки задержек (можно переопределить в config.py)
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
            import time
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
    
    
    
    def parse_all_films(self) -> List[Dict]:
        """
        Парсит все доступные данные о фильмах
        
        Returns:
            Список всех найденных фильмов
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        films = []
        
        # Извлекаем ID фильмов из ссылок (data-tid="23a2a59")
        film_links = self.soup.find_all('a', {'data-tid': '23a2a59'})
        print(f"🔍 Найдено {len(film_links)} ссылок с data-tid='23a2a59'")
        
        valid_links = 0
        invalid_links = 0
        
        for i, link in enumerate(film_links):
            href = link.get('href')
            print(f"  [{i+1}] href: {href}")
            
            if href and '/film/' in href:
                valid_links += 1
                # Извлекаем ID из URL /film/535341/ -> 535341
                href_parts = href.split('/film/')
                if len(href_parts) > 1:
                    film_id = href_parts[1].rstrip('/')
                    
                    # Ищем название фильма в атрибуте alt изображения
                    film_name = None
                    img = link.find('img')
                    if img and img.get('alt'):
                        film_name = img.get('alt').strip()
                    
                    film_data = {'id': film_id}
                    if film_name:
                        film_data['name'] = film_name
                    
                    films.append(film_data)
                    print(f"    ✅ Добавлен фильм: {film_id} - {film_name}")
                else:
                    print(f"    ❌ Не удалось извлечь ID из: {href}")
            else:
                invalid_links += 1
                print(f"    ❌ Некорректная ссылка: {href}")
        
        print(f"📊 Статистика:")
        print(f"   Всего ссылок: {len(film_links)}")
        print(f"   Валидных ссылок: {valid_links}")
        print(f"   Некорректных ссылок: {invalid_links}")
        print(f"   Обработано фильмов: {len(films)}")
        
        print(f"📊 Обработано {len(films)} фильмов")
        return films
    
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
