#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для страницы новостей на Кинопоиске
Извлекает информацию о новостях кино
"""

import os
import time
from typing import List, Dict
from bs4 import BeautifulSoup
from .base_parser import BaseParser


class NewsPageParser(BaseParser):
    """Парсер для страницы новостей"""
    
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
            
        return super().load_html_from_file(file_path)
    
    def load_html_from_url(self, url: str) -> BeautifulSoup:
        """Загружает HTML с веб-страницы Кинопоиска"""
        allowed_prefixes = (
            'https://www.kinopoisk.ru/media/',
            'https://www.kinopoisk.ru/media/news/',
            'https://www.kinopoisk.ru/media/article/',
        )
        return super().load_html_from_url(url, allowed_prefixes=allowed_prefixes)
    
    
    
    
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
                news_data['image_url'] = img_elem.get('src', '')
            
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
                news_data['publish_date'] = date_elem.get_text(strip=True)
            
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
                news_data['image_url'] = img_elem.get('src', '')
            
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
                news_data['publish_date'] = date_elem.get_text(strip=True)
            
            news_data['card_type'] = 'feature'
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге широкой карточки: {e}")
        
        return news_data
    
    
    def save_to_json(self, news_data: Dict, output_file: str = 'output/news_details.json'):
        """Сохраняет данные о новостях в JSON файл"""
        super().save_to_json(news_data, output_file)
    
    
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
