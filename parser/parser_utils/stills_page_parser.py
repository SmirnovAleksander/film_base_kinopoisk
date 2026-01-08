#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер галереи кадров/постеров на странице фильма Кинопоиска
Извлекает список URL изображений и доступных категорий
"""

import os
import re
from typing import List, Dict
from bs4 import BeautifulSoup
from .base_parser import BaseParser


class StillsPageParser(BaseParser):
    """Парсер страницы кадров/постеров фильма"""
    
    def load_html_from_url(self, url: str) -> BeautifulSoup:
        """Загружает HTML с веб-страницы Кинопоиска"""
        return super().load_html_from_url(url)
    
    def extract_image_urls(self) -> List[str]:
        if not self.soup:
            raise ValueError("HTML не загружен")
        urls: List[str] = []
        # Ищем все теги img на странице галереи
        for img in self.soup.find_all('img'):
            chosen = None
            # Предпочитаем srcset — пробуем выбрать самое большое изображение
            srcset = img.get('srcset')
            if srcset:
                # формат: url 1x, url 2x ... или url 300w, url 800w
                pairs = [p.strip() for p in srcset.split(',') if p.strip()]
                best = None
                for p in pairs:
                    parts = p.split()
                    if parts:
                        url = parts[0]
                        best = url  # последний обычно самый большой
                chosen = best
            if not chosen and img.get('src'):
                chosen = img.get('src')
            if not chosen:
                continue
            # Нормализуем URL
            if chosen.startswith('//'):
                chosen = 'https:' + chosen
            elif not chosen.startswith('http'):
                chosen = 'https://' + chosen
            if chosen not in urls:
                urls.append(chosen)
        return urls
    
    def extract_image_categories(self) -> List[Dict[str, str]]:
        if not self.soup:
            raise ValueError("HTML не загружен")
        
        categories = []
        
        # Ищем контейнер с навигацией категорий по data-tid="3b1075e9"
        nav_container = self.soup.find('ul', {'data-tid': '3b1075e9'})
        if not nav_container:
            # Альтернативный поиск по классу
            nav_container = self.soup.find('ul', class_=lambda x: x and 'imagesTypes' in x)
        
        if not nav_container:
            return categories
        
        # Ищем все элементы категорий по data-tid="70e06bb9"
        category_items = nav_container.find_all('li', {'data-tid': '70e06bb9'})
        
        for item in category_items:
            # Ищем ссылку на категорию
            link = item.find('a', {'data-test-id': 'next-link'})
            if not link or not link.get('href'):
                continue
            
            href = link.get('href').strip()
            
            # Извлекаем название категории
            name_elem = item.find('div', class_=lambda x: x and 'name' in x)
            name = name_elem.get_text(strip=True) if name_elem else ''
            
            # Извлекаем количество элементов
            count_elem = item.find('div', class_=lambda x: x and 'count' in x)
            count = count_elem.get_text(strip=True) if count_elem else ''
            
            # Определяем тип на основе URL
            category_type = self._determine_category_type(href)
            
            if href and name and category_type:
                categories.append({
                    'url': href,
                    'name': name,
                    'count': count,
                    'type': category_type
                })
        
        return categories
    
    def _determine_category_type(self, url: str) -> str:
        """
        Определяет тип категории напрямую из URL, извлекая сегмент после /film/{id}/
        
        Args:
            url: URL категории (например, '/film/1143242/stills/' или '/film/1143242/gallery/')
            
        Returns:
            Тип категории (например, 'stills', 'gallery', 'images', etc.)
        """
        if not url:
            return 'unknown'
        
        # Извлекаем тип из URL после /film/ID/
        # URL может быть: /film/1143242/stills/ или /film/1143242/gallery/
        import re
        match = re.search(r'/film/\d+/([^/]+)/', url)
        if match:
            return match.group(1)
        
        # Если не удалось извлечь, возвращаем последний сегмент пути
        path_parts = url.strip('/').split('/')
        if path_parts:
            return path_parts[-1]
        
        return 'unknown'
    
    def extract_stills_info(self, category_type: str = None) -> List[Dict]:
        """
        Извлекает структурированную информацию по каждой карточке кадра:
        - id (например, 1877733 из /picture/1877733/)
        - original (orig из b8279232)
        - type (тип категории: 'stills', 'shooting', 'posters')
        
        Args:
            category_type: Тип категории ('stills', 'shooting', 'posters')
            
        Returns:
            Список словарей с информацией о кадрах
        """
        if not self.soup:
            raise ValueError("HTML не загружен")
        
        items: List[Dict] = []
        # Каждая карточка кадра
        for card in self.soup.find_all('div', {'data-tid': 'c17ba3a'}):
            data: Dict = {}
            # Ссылка на страницу картинки /picture/{id}/
            link = card.find('a', {'data-test-id': 'next-link'})
            if link and link.get('href'):
                href = link.get('href').strip()
                # Извлекаем id картинки
                try:
                    m = re.search(r"/picture/(\d+)/", href)
                    if m:
                        data['id'] = m.group(1)
                except Exception:
                    pass

            # Превью из d813cf42 игнорируем (preview_1x/preview_2x не сохраняем)

            # Оригинал из a[data-tid="b8279232"]
            a_orig = card.find('a', {'data-tid': 'b8279232'})
            original = a_orig.get('href').strip() if a_orig and a_orig.get('href') else None

            # Ничего не добавляем для превью
            if original:
                data['original'] = super()._normalize_url(original)
            
            # Добавляем тип категории если указан
            if category_type:
                data['type'] = category_type

            if any(k in data for k in ('id', 'original', 'type')):
                items.append(data)

        return items

    def save_to_json(self, urls: List[str], output_file: str = 'output/stills_urls.json'):
        """Сохраняет список URL изображений в JSON"""
        super().save_to_json(urls, output_file)


def main():
    """Демо запуск: чтение локального HTML и вывод количества изображений"""
    parser = StillsPageParser()
    html_path = 'templates/posters_page.html'
    if os.path.exists(html_path):
        parser.load_html_from_file(html_path)
        urls = parser.extract_image_urls()
        parser.save_to_json(urls, 'output/stills_local_urls.json')
        print(f"Найдено изображений: {len(urls)}")
    else:
        print(f"Файл {html_path} не найден")


if __name__ == '__main__':
    main()
