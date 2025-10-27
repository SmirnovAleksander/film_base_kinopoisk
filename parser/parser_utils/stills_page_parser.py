#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер галереи кадров/постеров на странице фильма Кинопоиска
Извлекает список URL изображений
"""

import json
import os
import time
from typing import List, Dict
from bs4 import BeautifulSoup
import requests


class StillsPageParser:
    """Парсер страницы кадров/постеров фильма"""
    
    DELAY_BEFORE_REQUEST = 2
    
    def __init__(self, html_file_path: str = None):
        self.html_file_path = html_file_path
        self.soup = None
    
    def load_html_from_file(self, file_path: str = None) -> BeautifulSoup:
        if file_path:
            self.html_file_path = file_path
        if not self.html_file_path:
            raise ValueError("Не указан путь к HTML файлу")
        with open(self.html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        self.soup = BeautifulSoup(html, 'lxml')
        return self.soup
    
    def load_html_from_url(self, url: str) -> BeautifulSoup:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://www.kinopoisk.ru/'
            }
            session = requests.Session()
            session.headers.update(headers)
            self._load_cookies(session)
            time.sleep(self.DELAY_BEFORE_REQUEST)
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            if 'SmartCaptcha' in resp.text or 'робот' in resp.text.lower():
                return self._handle_captcha(session, url)
            self.soup = BeautifulSoup(resp.content, 'lxml')
            return self.soup
        except Exception as e:
            raise Exception(f"Ошибка при загрузке HTML с URL: {e}")
    
    def _load_cookies(self, session: requests.Session):
        try:
            cookies_file = 'parser_utils/cookies/session.json'
            if os.path.exists(cookies_file):
                with open(cookies_file, 'r', encoding='utf-8') as f:
                    cookies_data = json.load(f)
                if 'cookies' in cookies_data:
                    for name, value in cookies_data['cookies'].items():
                        session.cookies.set(name, value, domain='.kinopoisk.ru')
                elif isinstance(cookies_data, list):
                    for cookie in cookies_data:
                        session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.kinopoisk.ru'))
        except Exception:
            pass
    
    def _handle_captcha(self, session: requests.Session, url: str) -> BeautifulSoup:
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        r = session.get(url, timeout=30)
        self.soup = BeautifulSoup(r.content, 'lxml')
        return self.soup
    
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

    def extract_stills_info(self) -> List[Dict]:
        """
        Извлекает структурированную информацию по каждой карточке кадра:
        - id (например, 1877733 из /picture/1877733/)
        - original (orig из b8279232)
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
                    import re
                    m = re.search(r"/picture/(\d+)/", href)
                    if m:
                        data['id'] = m.group(1)
                except Exception:
                    pass

            # Превью из d813cf42 игнорируем (preview_1x/preview_2x не сохраняем)

            # Оригинал из a[data-tid="b8279232"]
            a_orig = card.find('a', {'data-tid': 'b8279232'})
            original = a_orig.get('href').strip() if a_orig and a_orig.get('href') else None

            # Нормализация URL-ов
            def normalize(u: str) -> str:
                if not u:
                    return u
                if u.startswith('//'):
                    return 'https:' + u
                if not u.startswith('http'):
                    return 'https://' + u
                return u

            # Ничего не добавляем для превью
            if original:
                data['original'] = normalize(original)

            if any(k in data for k in ('id', 'original')):
                items.append(data)

        return items

    def save_to_json(self, urls: List[str], output_file: str = 'output/stills_urls.json'):
        """Сохраняет список URL изображений в JSON"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(urls, f, ensure_ascii=False, indent=2)


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


