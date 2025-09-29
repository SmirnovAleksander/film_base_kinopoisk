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
        actor_data = {}
        
        # Извлекаем основное имя актера (data-tid="f22e0093")
        name_elem = self.soup.find('h1', {'data-tid': 'f22e0093'})
        if name_elem:
            actor_data['name'] = name_elem.get_text(strip=True)
        
        # Извлекаем английское имя актера (data-tid="7cdbd36a")
        english_name_elem = self.soup.find('div', {'data-tid': '7cdbd36a'})
        if english_name_elem:
            actor_data['english_name'] = english_name_elem.get_text(strip=True)
        
        # Извлекаем карьеру/роли (data-test-id="career")
        career_elem = self.soup.find('div', {'data-test-id': 'career'})
        if career_elem:
            # Находим все кнопки с ролями (data-tid="e150c550")
            role_buttons = career_elem.find_all('button', {'data-tid': 'e150c550'})
            roles = []
            for button in role_buttons:
                role_text = button.get_text(strip=True)
                if role_text:
                    roles.append(role_text)
            
            if roles:
                actor_data['career'] = roles
        
        # Извлекаем жанры (контейнер data-tid="e32f6be5", кнопки data-tid="9758b27c")
        genres_container = self.soup.find('div', {'data-tid': 'e32f6be5'})
        if genres_container:
            genre_buttons = genres_container.find_all('button', {'data-tid': '9758b27c'})
            genres = []
            for btn in genre_buttons:
                text = btn.get_text(strip=True)
                if text:
                    genres.append(text)
            if genres:
                actor_data['genres'] = genres
        
        # Извлекаем рост (data-test-id="height")
        height_elem = self.soup.find('div', {'data-test-id': 'height'})
        if height_elem:
            height_div = height_elem.find('div', {'data-tid': 'e1e37c21'})
            if height_div:
                height_text = height_div.get_text(strip=True)
                # Конвертируем метры в сантиметры
                if 'м' in height_text:
                    try:
                        # Извлекаем число из строки типа "1.9 м"
                        height_value = float(height_text.replace(' м', '').replace('м', ''))
                        # Конвертируем в сантиметры
                        height_cm = int(height_value * 100)
                        actor_data['height'] = str(height_cm)
                    except ValueError:
                        actor_data['height'] = height_text
                else:
                    actor_data['height'] = height_text
        
        # Извлекаем дату рождения (data-test-id="birthday")
        birthday_elem = self.soup.find('div', {'data-test-id': 'birthday'})
        if birthday_elem:
            birthday_div = birthday_elem.find('div', {'data-tid': '71455188'})
            if birthday_div:
                # Извлекаем отдельные компоненты
                day_month_link = birthday_div.find('a', href=lambda x: x and 'birthday' in x and 'day' in x and 'month' in x)
                if day_month_link:
                    actor_data['birthday_day_month'] = day_month_link.get_text(strip=True)
                
                year_link = birthday_div.find('a', href=lambda x: x and 'birthday' in x and 'year' in x)
                if year_link:
                    actor_data['birthday_year'] = year_link.get_text(strip=True)
                
                zodiac_link = birthday_div.find('a', href=lambda x: x and 'zodiac' in x)
                if zodiac_link:
                    actor_data['zodiac'] = zodiac_link.get_text(strip=True)
                
                # Извлекаем возраст
                age_span = birthday_div.find('span', class_='styles_valueDark__jsGKY')
                if age_span:
                    age_text = age_span.get_text(strip=True)
                    # Извлекаем только число из "47 лет"
                    import re
                    age_match = re.search(r'(\d+)', age_text)
                    if age_match:
                        actor_data['age'] = age_match.group(1)
        
        # Извлекаем место рождения (data-test-id="placeOfBirthday")
        birthplace_elem = self.soup.find('div', {'data-test-id': 'placeOfBirthday'})
        if birthplace_elem:
            birthplace_div = birthplace_elem.find('div', {'data-tid': '222c6c05'})
            if birthplace_div:
                # Извлекаем все ссылки с местами
                location_links = birthplace_div.find_all('a', {'data-tid': '46e19321'})
                locations = []
                for link in location_links:
                    location_text = link.get_text(strip=True)
                    if location_text:
                        locations.append(location_text)
                
                if locations:
                    actor_data['birthplace'] = locations
        
        # Извлекаем семейную информацию (data-test-id="partner")
        partner_elem = self.soup.find('div', {'data-test-id': 'partner'})
        if partner_elem:
            partner_ul = partner_elem.find('ul', {'data-tid': 'eb7e5e48'})
            if partner_ul:
                partner_lis = partner_ul.find_all('li', {'data-tid': '4f89888f'})
                spouse_names = []
                children_list = []
                for li in partner_lis:
                    # Имя(я) могут быть ссылкой <a> или <span>
                    name_link = li.find('a', {'data-test-id': 'next-link'})
                    name_text = ''
                    if name_link:
                        name_text = name_link.get_text(strip=True)
                    else:
                        name_span = li.find('span', class_='styles_valueDark__jsGKY')
                        if name_span:
                            name_text = name_span.get_text(strip=True)
                    if name_text:
                        spouse_names.append(name_text)
                    # Количество детей
                    children_span = li.find('span', class_='styles_childrenCount__L7a53')
                    if children_span:
                        children_list.append(children_span.get_text(strip=True))
                if spouse_names:
                    actor_data['spouse'] = spouse_names
                if children_list:
                    actor_data['children'] = children_list
        
        # Извлекаем статистику фильмографии (data-test-id="filmographyTotal")
        filmography_elem = self.soup.find('div', {'data-test-id': 'filmographyTotal'})
        if filmography_elem:
            filmography_div = filmography_elem.find('div', {'data-tid': '16f1da45'})
            if filmography_div:
                # Извлекаем общее количество фильмов
                total_span = filmography_div.find('span')
                if total_span:
                    total_text = total_span.get_text(strip=True)
                    if total_text.isdigit():
                        actor_data['total_films'] = int(total_text)
                
                # Извлекаем годы работы
                year_buttons = filmography_div.find_all('button', {'data-tid': '10653ce8'})
                if len(year_buttons) >= 2:
                    start_year = year_buttons[0].get_text(strip=True)
                    end_year = year_buttons[1].get_text(strip=True)
                    
                    # Сохраняем отдельные поля для БД
                    try:
                        actor_data['career_start_year'] = int(start_year)
                        actor_data['career_end_year'] = int(end_year)
                        # Вычисляем продолжительность карьеры
                        career_duration = int(end_year) - int(start_year)
                        actor_data['career_duration'] = career_duration
                    except ValueError:
                        pass
        
        # Извлекаем фото актера (data-tid="d813cf42")
        photo_elem = self.soup.find('img', {'data-tid': 'd813cf42'})
        if photo_elem and photo_elem.get('src'):
            photo_url = photo_elem.get('src')
            # Нормализуем URL - добавляем https:// если нужно
            if photo_url.startswith('//'):
                photo_url = 'https:' + photo_url
            elif not photo_url.startswith('http'):
                photo_url = 'https://' + photo_url
            actor_data['photo'] = photo_url
        
        return actor_data
    
    def _extract_from_meta(self) -> Dict:
        """Извлекает данные из meta тегов"""
        # TODO: Добавить парсинг meta тегов
        return {}
    
    def save_to_json(self, actor_data: Dict, output_file: str = 'output/actor_details.json'):
        """
        Сохраняет данные об актере в JSON файл (ОТКЛЮЧЕНО)
        
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
