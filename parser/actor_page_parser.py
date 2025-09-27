#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для страницы актера на Кинопоиске
Извлекает детальную информацию об актере
"""

import json
import os
import re
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import requests


class ActorPageParser:
    """Парсер для страницы актера"""
    
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
    
    def extract_actor_details(self) -> Dict:
        """
        Извлекает детальную информацию об актере из HTML элементов
        
        Returns:
            Словарь с детальной информацией об актере
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        actor_data = {}
        
        # Извлекаем данные из HTML элементов
        html_data = self._extract_from_html()
        if html_data:
            actor_data.update(html_data)
        
        # Извлекаем данные из meta тегов
        meta_data = self._extract_from_meta()
        if meta_data:
            actor_data.update(meta_data)
        
        return actor_data
    
    def _extract_from_html(self) -> Dict:
        """Извлекает данные из HTML элементов"""
        # TODO: Добавить парсинг HTML элементов
        return {}
    
    def _extract_from_meta(self) -> Dict:
        """Извлекает данные из meta тегов"""
        # TODO: Добавить парсинг meta тегов
        return {}
    
    def save_to_json(self, actor_data: Dict, output_file: str = 'output/actor_details.json'):
        """
        Сохраняет данные об актере в JSON файл
        
        Args:
            actor_data: Данные об актере для сохранения
            output_file: Путь к выходному файлу
        """
        try:
            # Создаем папку output если её нет
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(actor_data, file, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в файл: {output_file}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    
    def print_actor_details(self, actor_data: Dict):
        """
        Выводит детальную информацию об актере
        
        Args:
            actor_data: Данные об актере
        """
        print("\n=== Детальная информация об актере ===")
        print("-" * 50)
        
        # Основная информация
        if actor_data.get('name'):
            print(f"🎭 Имя: {actor_data['name']}")
        
        if actor_data.get('full_name'):
            print(f"📝 Полное имя: {actor_data['full_name']}")
        
        if actor_data.get('birth_date'):
            print(f"🎂 Дата рождения: {actor_data['birth_date']}")
        
        if actor_data.get('birth_place'):
            print(f"🌍 Место рождения: {actor_data['birth_place']}")
        
        if actor_data.get('nationality'):
            print(f"🏳️ Национальность: {actor_data['nationality']}")
        
        if actor_data.get('height'):
            print(f"📏 Рост: {actor_data['height']}")
        
        # Профессии
        if actor_data.get('profession'):
            professions = actor_data['profession']
            if isinstance(professions, list):
                print(f"💼 Профессии: {', '.join(professions)}")
            else:
                print(f"💼 Профессия: {professions}")
        
        # Фильмография
        if actor_data.get('filmography'):
            films = actor_data['filmography']
            print(f"\n🎬 Фильмография ({len(films)} фильмов):")
            for i, film in enumerate(films[:10], 1):  # Показываем первые 10
                title = film.get('title', 'Неизвестно')
                year = film.get('year', '')
                role = film.get('role', '')
                year_str = f" ({year})" if year else ""
                role_str = f" - {role}" if role else ""
                print(f"  {i}. {title}{year_str}{role_str}")
            
            if len(films) > 10:
                print(f"    ... и еще {len(films) - 10} фильмов")
        
        # Награды
        if actor_data.get('awards'):
            awards = actor_data['awards']
            if isinstance(awards, list):
                print(f"\n🏆 Награды: {', '.join(awards[:5])}")
                if len(awards) > 5:
                    print(f"    ... и еще {len(awards) - 5} наград")
            else:
                print(f"🏆 Награды: {awards}")
        
        # Образование
        if actor_data.get('education'):
            print(f"🎓 Образование: {actor_data['education']}")
        
        # Биография
        if actor_data.get('biography'):
            bio = actor_data['biography']
            if len(bio) > 300:
                bio = bio[:300] + "..."
            print(f"\n📖 Биография: {bio}")
        
        print()


def main():
    """Основная функция для демонстрации работы парсера"""
    parser = ActorPageParser()
    
    try:
        # Загружаем HTML из файла
        print("Загружаем HTML файл...")
        parser.load_html_from_file('templates/actor_page_kinopoisk.html')
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию об актере...")
        actor_data = parser.extract_actor_details()
        
        # Выводим результаты
        parser.print_actor_details(actor_data)
        
        # Сохраняем в JSON
        parser.save_to_json(actor_data, 'output/actor_details.json')
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
