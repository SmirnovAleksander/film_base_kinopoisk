#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для страницы новостей на Кинопоиске
Извлекает информацию о новостях кино
"""

import json
import os
import time
from typing import List, Dict
from bs4 import BeautifulSoup
import requests


class NewsPageParser:
    """Парсер для страницы новостей"""
    
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
        # Разрешаем парсинг только для допустимых доменов/путей
        allowed_prefixes = (
            'https://www.kinopoisk.ru/media/',
            'https://www.kinopoisk.ru/media/news/',
            'https://www.kinopoisk.ru/media/article/',
        )
        if not any(url.startswith(p) for p in allowed_prefixes):
            raise ValueError("URL не поддерживается этим парсером. Допустимы только /media, /media/news, /media/article")

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
            cookies_file = 'parser_utils/cookies/session.json'
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
    
    
    
    
    def parse_news_list(self) -> List[Dict]:
        """
        Парсит список новостей со страницы
        
        Returns:
            List[Dict]: Список новостей с информацией
        """
        if not self.soup:
            print("❌ HTML не загружен")
            return []
        
        news_list = []
        
        try:
            # Парсим обычные карточки новостей (data-tid="a436d48b")
            regular_articles = self.soup.find_all('article', {'data-tid': 'a436d48b'})
            for article in regular_articles:
                news_data = self.parse_news_item(article)
                if news_data:
                    news_list.append(news_data)
            
            # Парсим широкие карточки новостей (data-tid="e27fe2d7")
            feature_articles = self.soup.find_all('article', {'data-tid': 'e27fe2d7'})
            for article in feature_articles:
                news_data = self.parse_news_item(article)
                if news_data:
                    news_list.append(news_data)
            
            return news_list
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге новостей: {e}")
            return []
    
    def parse_multiple_pages(self, pages_count: int = 5, content_type: str = 'news') -> List[Dict]:
        """
        Парсит контент с нескольких страниц
        
        Args:
            pages_count: Количество страниц для парсинга
            content_type: Тип контента (news, video, game, podcast)
            
        Returns:
            List[Dict]: Список всего контента с всех страниц
        """
        all_content = []
        
        # Определяем базовый URL в зависимости от типа контента
        # Разрешённые только типы media/news и media/article, media (лендинг)
        if content_type not in ('news', 'article', 'media'):
            content_type = 'news'
        base_url = 'https://www.kinopoisk.ru/media/news/' if content_type == 'news' else (
            'https://www.kinopoisk.ru/media/article/' if content_type == 'article' else 'https://www.kinopoisk.ru/media/'
        )
        
        try:
            for page_num in range(1, pages_count + 1):
                print(f"📄 Парсинг страницы {page_num}/{pages_count} ({content_type})")
                
                # Формируем URL для страницы
                if page_num == 1:
                    page_url = base_url
                else:
                    page_url = f"{base_url}?page={page_num}"
                
                # Загружаем страницу
                self.load_html_from_url(page_url)
                
                if self.soup:
                    # Парсим контент с текущей страницы
                    page_content = self.parse_news_list()
                    
                    # Добавляем тип контента к каждому элементу
                    for item in page_content:
                        item['type'] = content_type
                    
                    all_content.extend(page_content)
                    print(f"✅ Страница {page_num}: найдено {len(page_content)} элементов ({content_type})")
                else:
                    print(f"❌ Не удалось загрузить страницу {page_num}")
                
                # Небольшая задержка между запросами
                if page_num < pages_count:
                    time.sleep(2)
            
            print(f"📊 Всего найдено элементов ({content_type}): {len(all_content)}")
            return all_content
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге нескольких страниц: {e}")
            return all_content
    
    def parse_news_item(self, news_element) -> Dict:
        """
        Парсит отдельную новость
        
        Args:
            news_element: BeautifulSoup элемент новости
            
        Returns:
            Dict: Информация о новости
        """
        news_data = {}
        
        try:
            # Определяем тип карточки по data-tid
            card_type = news_element.get('data-tid', '')
            
            if card_type == 'a436d48b':  # Обычная карточка
                news_data = self._parse_regular_card(news_element)
            elif card_type == 'e27fe2d7':  # Широкая карточка
                news_data = self._parse_feature_card(news_element)
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге новости: {e}")
        
        return news_data
    
    def _parse_regular_card(self, article) -> Dict:
        """Парсит обычную карточку новости"""
        news_data = {}
        
        try:
            # Ссылка на новость
            link_elem = article.find('a', class_='rHg73hUuhIU9jiVJ6itV')
            if link_elem:
                href = link_elem.get('href', '')
                if href.startswith('/'):
                    news_data['url'] = f"https://www.kinopoisk.ru{href}"
                else:
                    news_data['url'] = href
                news_data['title'] = link_elem.get('aria-label', '')
            
            # Изображение
            img_elem = article.find('img', {'data-tid': 'd813cf42'})
            if img_elem:
                news_data['image'] = img_elem.get('src', '')
            
            # Категория (data-tid="b66cdd18" внутри data-tid="543e842b")
            category_wrapper = article.find('div', {'data-tid': '543e842b'})
            if category_wrapper:
                category_elem = category_wrapper.find('span', {'data-tid': 'b66cdd18'})
                if category_elem:
                    news_data['category'] = category_elem.get_text(strip=True)
                else:
                    # Фолбэк: категория может быть ссылкой <a> внутри этого же блока
                    link_cat = category_wrapper.find('a')
                    if link_cat and link_cat.get_text(strip=True):
                        news_data['category'] = link_cat.get_text(strip=True)
            
            # Заголовок: в <h3> первый span — лейбл (например, «Подкаст»), его игнорируем
            if category_wrapper:
                title_elem = category_wrapper.find_next('h3')
                if title_elem:
                    spans = title_elem.find_all('span')
                    if spans:
                        if len(spans) > 1:
                            title_text = " ".join(s.get_text(strip=True) for s in spans[1:] if s.get_text(strip=True))
                        else:
                            title_text = spans[0].get_text(strip=True)
                        if title_text:
                            news_data['title'] = title_text
            
            # Дата
            date_elem = article.find('span', class_='NUIoouHmDcRbqxQpQ8v8')
            if date_elem:
                news_data['date'] = date_elem.get_text(strip=True)
            
            news_data['card_type'] = 'regular'
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге обычной карточки: {e}")
        
        return news_data
    
    def _parse_feature_card(self, article) -> Dict:
        """Парсит широкую карточку новости"""
        news_data = {}
        
        try:
            # Ссылка на новость
            link_elem = article.find('a', class_='post-feature-card__link')
            if link_elem:
                href = link_elem.get('href', '')
                if href.startswith('/'):
                    news_data['url'] = f"https://www.kinopoisk.ru{href}"
                else:
                    news_data['url'] = href
                news_data['title'] = link_elem.get('aria-label', '')
            
            # Изображение
            img_elem = article.find('img', {'data-tid': 'd813cf42'})
            if img_elem:
                news_data['image'] = img_elem.get('src', '')
            
            # Категория (data-tid="b66cdd18" внутри data-tid="543e842b")
            category_wrapper = article.find('div', {'data-tid': '543e842b'})
            if category_wrapper:
                category_elem = category_wrapper.find('span', {'data-tid': 'b66cdd18'})
                if category_elem:
                    news_data['category'] = category_elem.get_text(strip=True)
            
            # Заголовок
            title_elem = article.find('h3', class_='post-feature-card__title')
            if title_elem:
                news_data['title'] = title_elem.get_text(strip=True)
            
            # Дата
            date_elem = article.find('span', class_='post-feature-card__published-date')
            if date_elem:
                news_data['date'] = date_elem.get_text(strip=True)
            
            news_data['card_type'] = 'feature'
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге широкой карточки: {e}")
        
        return news_data
    
    
    def save_to_json(self, news_data: Dict, output_file: str = 'output/news_details.json'):
        """
        Сохраняет данные о новостях в JSON файл
        
        Args:
            news_data: Данные о новостях для сохранения
            output_file: Путь к выходному файлу
        """
        try:
            # Создаем папку output если её нет
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(news_data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    
    
def main():
    """Основная функция для тестирования парсера"""
    print("🚀 Запуск парсера новостей Кинопоиска")
    
    # Создаем парсер
    parser = NewsPageParser()
    
    # Загружаем HTML из файла если он существует
    html_file = "templates/news_page.html"
    if os.path.exists(html_file):
        print(f"📁 Загружаем HTML из файла: {html_file}")
        parser.load_html_from_file(html_file)
    else:
        print(f"🌐 Загружаем HTML с URL")
        parser.load_html_from_url("https://www.kinopoisk.ru/media/news/")
    
    if parser.soup:
        # Парсим новости
        news_list = parser.parse_news_list()
        
        # Собираем все данные
        result = {
            'news_list': news_list,
            'parsed_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_news': len(news_list)
        }
        
        # Сохраняем результат
        parser.save_to_json(result, 'output/news_details.json')
        
        print(f"\n✅ Парсинг завершен. Найдено новостей: {len(news_list)}")
    else:
        print("❌ Не удалось загрузить HTML")


if __name__ == "__main__":
    main()
