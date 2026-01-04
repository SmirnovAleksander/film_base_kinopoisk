#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для страницы отдельного фильма на Кинопоиске
Извлекает детальную информацию о фильме
"""

import json
import os
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base_parser import BaseParser


class SerialPageParser(BaseParser):
    """Парсер для страницы отдельного фильма"""
    
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
        return super().load_html_from_url(url)
    
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
            
        # Извлекаем описание (data-tid="bfd38da2")
        description_elem = self.soup.find('p', {'data-tid': 'bfd38da2'})
        if description_elem:
            film_data['description'] = description_elem.get_text(strip=True)
        
        
        # Извлекаем рейтинг Кинопоиска (data-tid="939058a8")
        kp_rating_elem = self.soup.find('span', {'data-tid': '939058a8'})
        if kp_rating_elem:
            film_data['rating_kp'] = kp_rating_elem.get_text(strip=True)
        
        # Извлекаем количество оценок Кинопоиска
        kp_count_elem = self.soup.find('span', class_='styles_count__mJ4RS')
        if kp_count_elem:
            kp_count_text = kp_count_elem.get_text(strip=True)
            # Извлекаем только число из "2 607 836 оценок"
            kp_count_match = re.search(r'([\d\s]+)', kp_count_text)
            if kp_count_match:
                # Убираем пробелы и сохраняем как число
                kp_count = kp_count_match.group(1).replace(' ', '')
                film_data['kp_votes_count'] = kp_count
        
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
            imdb_count_text = imdb_count_elem.get_text(strip=True)
            # Извлекаем только число из "995 000 оценок"
            imdb_count_match = re.search(r'([\d\s]+)', imdb_count_text)
            if imdb_count_match:
                # Убираем пробелы и сохраняем как число
                imdb_count = imdb_count_match.group(1).replace(' ', '')
                film_data['imdb_votes_count'] = imdb_count
        
        # Извлекаем постер (поиск по классу film-poster и data-tid)
        poster_elem = None
        
        # Сначала ищем по классу film-poster
        poster_elem = self.soup.find('img', class_=lambda x: x and 'film-poster' in x)
        
        # Если не найден, ищем по data-tid
        if not poster_elem:
            poster_elem = self.soup.find('img', {'data-tid': 'd813cf42'})
        
        if poster_elem:
            poster_url = None
            
            # Приоритет: изображение 600x900 > srcset > src
            if poster_elem.get('srcset'):
                # Парсим srcset и ищем изображение 300x450
                srcset = poster_elem.get('srcset')
                
                # Сначала ищем URL с 300x450 в srcset
                srcset_urls = re.findall(r'([^\s]+)\s+(\d+)x', srcset)
                poster_url = None
                
                # Ищем URL с 600x900 (1x множитель)
                for url, multiplier in srcset_urls:
                    if '600x900' in url and multiplier == '1':
                        poster_url = url
                        break
                
                # Если 600x900 не найден, берем первый доступный
                if not poster_url and srcset_urls and len(srcset_urls) > 0:
                    poster_url = srcset_urls[0][0]
            
            # Если srcset не найден, используем src
            if not poster_url and poster_elem.get('src'):
                src_url = poster_elem.get('src')
                # Предпочитаем URL с 600x900
                if '600x900' in src_url:
                    poster_url = src_url
                else:
                    poster_url = src_url
            
            if poster_url:
                # Нормализуем URL - добавляем https:// если нужно
                if poster_url.startswith('//'):
                    poster_url = 'https:' + poster_url
                elif not poster_url.startswith('http'):
                    poster_url = 'https://' + poster_url
                film_data['poster'] = poster_url
        
        # # Извлекаем год производства (data-test-id="year")
        # year_elem = self.soup.find('div', {'data-test-id': 'year'})
        # if year_elem:
        #     year_link = year_elem.find('a')
        #     if year_link:
        #         film_data['year'] = year_link.get_text(strip=True)
        
        # # Извлекаем страны (data-test-id="countries")
        # countries_elem = self.soup.find('div', {'data-test-id': 'countries'})
        # if countries_elem:
        #     country_links = countries_elem.find_all('a')
        #     countries = [link.get_text(strip=True) for link in country_links]
        #     if countries:
        #         film_data['countries'] = countries
        
        # # Извлекаем жанры (data-test-id="genres")
        # genres_elem = self.soup.find('div', {'data-test-id': 'genres'})
        # if genres_elem:
        #     genre_links = genres_elem.find_all('a')
        #     genres = [link.get_text(strip=True) for link in genre_links if link.get_text(strip=True) != 'слова']
        #     if genres:
        #         film_data['genres'] = genres
        
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
                    href_parts = link.get('href').split('/name/')
                    if len(href_parts) > 1:
                        person_id = href_parts[1].rstrip('/')
                    else:
                        continue
                    directors.append({'name': name, 'id': person_id})
            if directors:
                film_data['directors'] = directors
        
        # # Извлекаем сценаристов (data-test-id="writers")
        # writers_elem = self.soup.find('div', {'data-test-id': 'writers'})
        # if writers_elem:
        #     writer_links = writers_elem.find_all('a')
        #     writers = []
        #     for link in writer_links:
        #         if link.get('href') and '/name/' in link.get('href'):
        #             name = link.get_text(strip=True)
        #             person_id = link.get('href').split('/name/')[1].rstrip('/')
        #             writers.append({'name': name, 'id': person_id})
        #     if writers:
        #         film_data['writers'] = writers
        
        # # Извлекаем продюсеров (data-test-id="producers")
        # producers_elem = self.soup.find('div', {'data-test-id': 'producers'})
        # if producers_elem:
        #     producer_links = producers_elem.find_all('a')
        #     producers = []
        #     for link in producer_links:
        #         if link.get('href') and '/name/' in link.get('href'):
        #             name = link.get_text(strip=True)
        #             person_id = link.get('href').split('/name/')[1].rstrip('/')
        #             producers.append({'name': name, 'id': person_id})
        #     if producers:
        #         film_data['producers'] = producers
        
        # # Извлекаем операторов (data-test-id="operators")
        # operators_elem = self.soup.find('div', {'data-test-id': 'operators'})
        # if operators_elem:
        #     operator_links = operators_elem.find_all('a')
        #     operators = []
        #     for link in operator_links:
        #         if link.get('href') and '/name/' in link.get('href'):
        #             name = link.get_text(strip=True)
        #             person_id = link.get('href').split('/name/')[1].rstrip('/')
        #             operators.append({'name': name, 'id': person_id})
        #     if operators:
        #         film_data['operators'] = operators
        
        # # Извлекаем композиторов (data-test-id="composers")
        # composers_elem = self.soup.find('div', {'data-test-id': 'composers'})
        # if composers_elem:
        #     composer_links = composers_elem.find_all('a')
        #     composers = []
        #     for link in composer_links:
        #         if link.get('href') and '/name/' in link.get('href'):
        #             name = link.get_text(strip=True)
        #             person_id = link.get('href').split('/name/')[1].rstrip('/')
        #             composers.append({'name': name, 'id': person_id})
        #     if composers:
        #         film_data['composers'] = composers
        
        # # Извлекаем художников (data-test-id="designers")
        # designers_elem = self.soup.find('div', {'data-test-id': 'designers'})
        # if designers_elem:
        #     designer_links = designers_elem.find_all('a')
        #     designers = []
        #     for link in designer_links:
        #         if link.get('href') and '/name/' in link.get('href'):
        #             name = link.get_text(strip=True)
        #             person_id = link.get('href').split('/name/')[1].rstrip('/')
        #             designers.append({'name': name, 'id': person_id})
        #     if designers:
        #         film_data['designers'] = designers
        
        # # Извлекаем монтажеров (data-test-id="filmEditors")
        # editors_elem = self.soup.find('div', {'data-test-id': 'filmEditors'})
        # if editors_elem:
        #     editor_links = editors_elem.find_all('a')
        #     editors = []
        #     for link in editor_links:
        #         if link.get('href') and '/name/' in link.get('href'):
        #             name = link.get_text(strip=True)
        #             person_id = link.get('href').split('/name/')[1].rstrip('/')
        #             editors.append({'name': name, 'id': person_id})
        #     if editors:
        #         film_data['editors'] = editors
        
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
        
        # Извлекаем платформу (data-tid="603f73a4")
        platform_elem = self.soup.find('a', {'data-tid': '603f73a4'})
        if platform_elem:
            platform_name = platform_elem.get_text(strip=True)
            if platform_name:
                film_data['platform'] = platform_name
        
        # # Извлекаем возрастной рейтинг (data-test-id="ageRestriction")
        # age_elem = self.soup.find('div', {'data-test-id': 'ageRestriction'})
        # if age_elem:
        #     age_span = age_elem.find('span', {'data-tid': '5c1ffa33'})
        #     if age_span:
        #         film_data['content_rating'] = age_span.get_text(strip=True)


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
                    href_parts = film_link.get('href').split('/film/')
                    if len(href_parts) > 1:
                        film_id = href_parts[1].rstrip('/')
                    else:
                        continue
                    
                    data_obj = {'id': film_id}
                    
                    # Извлекаем название фильма
                    title_span = item.find('span', {'data-tid': 'ecca3393'})
                    if title_span:
                        data_obj['title'] = title_span.get_text(strip=True)

                    # Пытаемся извлечь год (строго 19xx или 20xx как отдельное слово)
                    try:
                        year_text_candidates = item.stripped_strings
                        for t in year_text_candidates:
                            m = re.search(r'\b(19\d{2}|20\d{2})\b', t)
                            if m:
                                data_obj['year'] = m.group(1)
                                break
                    except Exception:
                        pass

                    # Пытаемся извлечь жанры: из текстов внутри карточки, разбивая по разделителям и фильтруя
                    try:
                        raw_tokens = []
                        for t in item.stripped_strings:
                            # разбиваем по типичным разделителям
                            parts = re.split(r'[•·,\/|]', t)
                            for p in parts:
                                token = p.strip()
                                if token:
                                    raw_tokens.append(token)
                        genres = []
                        title_val = (data_obj.get('title') or '').lower()
                        year_val = data_obj.get('year')
                        for tok in raw_tokens:
                            low = tok.lower()
                            # отсекаем явные не-жанровые токены
                            if low == '' or low == title_val:
                                continue
                            if year_val and year_val in tok:
                                continue
                            if re.search(r'\d', tok):  # содержит цифры
                                continue
                            # оставляем короткие жанровые слова/фразы
                            if any(ch.isalpha() for ch in tok):
                                genres.append(tok)
                        if genres:
                            # нормализуем, убираем дубликаты, оставляем до 5
                            seen = set()
                            uniq = []
                            for g in genres:
                                if g not in seen:
                                    seen.add(g)
                                    uniq.append(g)
                            if uniq:
                                data_obj['genres'] = uniq[:5]
                    except Exception:
                        pass

                    # Извлекаем картинку (постер превью) из первого img
                    img = item.find('img')
                    poster_url = None
                    if img:
                        if img.get('srcset'):
                            # берём последний элемент из srcset как наиболее крупный
                            parts = [p.strip() for p in img.get('srcset').split(',') if p.strip()]
                            if parts:
                                poster_url = parts[-1].split()[0]
                        if not poster_url and img.get('src'):
                            poster_url = img.get('src')
                    if poster_url:
                        if poster_url.startswith('//'):
                            poster_url = 'https:' + poster_url
                        elif not poster_url.startswith('http'):
                            poster_url = 'https://' + poster_url
                        data_obj['poster'] = poster_url

                    # Пытаемся извлечь рейтинг (первая встреченная дробь/число с точкой)
                    try:
                        rating_found = None
                        for t in item.stripped_strings:
                            m = re.search(r'\b(\d{1,2}(?:[\.,]\d)?)\b', t)
                            if m:
                                val = m.group(1).replace(',', '.')
                                # отфильтруем невозможные >10
                                try:
                                    if 0.0 <= float(val) <= 10.0:
                                        rating_found = val
                                        break
                                except Exception:
                                    pass
                        if rating_found is not None:
                            data_obj['rating'] = rating_found
                    except Exception:
                        pass

                    similar_films.append(data_obj)
            
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
                    href_parts = link.get('href').split('/name/')
                    if len(href_parts) > 1:
                        person_id = href_parts[1].rstrip('/')
                    else:
                        continue
                    actors.append({'name': name, 'id': person_id})
            
            if actors:
                film_data['actors'] = actors

        # Извлекаем провайдеров для просмотра (сторонние источники)


        providers: List[Dict] = []

        # Вариант 1: контейнер провайдеров data-tid="c456f2ce"
        providers_container = self.soup.find('div', {'data-tid': 'c456f2ce'})
        if providers_container:
            provider_links = providers_container.find_all('a', {'data-tid': '5f829942'})
            for a in provider_links:
                href = a.get('href')
                name_el = a.find('span', class_='styles_title__i15WC')
                name = name_el.get_text(strip=True) if name_el else None
                # Логотип внутри img с data-tid="d813cf42" или внутри .styles_logo__pS9vc
                logo_img = a.find('img', {'data-tid': 'd813cf42'}) or a.find('span', class_='styles_logo__pS9vc')
                logo_src = None
                if logo_img and hasattr(logo_img, 'get'):
                    logo_src = logo_img.get('src') if logo_img.name == 'img' else None
                    if logo_src is None:
                        inner_img = a.find('img')
                        logo_src = inner_img.get('src') if inner_img and inner_img.get('src') else None
                logo_url = self._normalize_url(logo_src) if logo_src else None
                if href and name:
                    providers.append({'name': name, 'url': href, 'logo': logo_url})

        # Вариант 2: если контейнер не найден, ищем все ссылки провайдеров по data-tid="5f829942" во всём документе
        if not providers:
            for a in self.soup.find_all('a', {'data-tid': '5f829942'}):
                href = a.get('href')
                name_el = a.find('span', class_='styles_title__i15WC')
                name = name_el.get_text(strip=True) if name_el else None
                logo_img = a.find('img', {'data-tid': 'd813cf42'}) or a.find('img')
                logo_src = logo_img.get('src') if logo_img and logo_img.get('src') else None
                logo_url = self._normalize_url(logo_src) if logo_src else None
                if href and name:
                    providers.append({'name': name, 'url': href, 'logo': logo_url})

        # Вариант 3: эвристика — ищем блоки с логотипом OTT (get-ott) и подписью названия
        if not providers:
            for a in self.soup.find_all('a', href=True):
                name_el = a.find('span', class_='styles_title__i15WC')
                img = a.find('img')
                if name_el and img and img.get('src') and ('get-ott' in img.get('src') or 'ott' in img.get('src')):
                    name = name_el.get_text(strip=True)
                    href = a.get('href')
                    logo_url = self._normalize_url(img.get('src'))
                    providers.append({'name': name, 'url': href, 'logo': logo_url})

        # Вариант 4: Парсинг из JSON (Apollo State)
        if not providers:
            json_providers = self._extract_watchability_from_json()
            if json_providers:
                providers.extend(json_providers)

        if providers:
            film_data['watch_providers'] = providers
        
        return film_data
    
    def _extract_watchability_from_json(self) -> List[Dict]:
        """Извлекает провайдеров из JSON данных (__NEXT_DATA__)"""
        providers = []
        try:
            # Ищем скрипт с id="__NEXT_DATA__"
            script = self.soup.find('script', id='__NEXT_DATA__')
            if not script or not script.string:
                return providers
            
            try:
                data = json.loads(script.string)
                
                # Рекурсивная функция для поиска ключа watchability
                def find_watchability(obj):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if key.startswith('watchability') and isinstance(value, dict):
                                if 'items' in value and isinstance(value['items'], list):
                                    return value
                            
                            # Рекурсивный поиск в значениях
                            if isinstance(value, (dict, list)):
                                result = find_watchability(value)
                                if result:
                                    return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = find_watchability(item)
                            if result:
                                return result
                    return None

                watchability = find_watchability(data.get('props', {}))

                if watchability and 'items' in watchability:
                    for item in watchability['items']:
                        if item.get('__typename') == 'Watchability':
                            platform = item.get('platform')
                            url = item.get('url')
                            
                            if platform and url:
                                name = platform.get('name')
                                logo = platform.get('logo')
                                avatars_url = logo.get('avatarsUrl') if logo else None
                                
                                if name:
                                    # Проверяем дубликаты
                                    if not any(p['name'] == name for p in providers):
                                        logo_url = self._normalize_url(avatars_url)
                                        if logo_url and not logo_url.endswith('/72x72'):
                                            logo_url = f"{logo_url}/72x72"
                                            
                                        providers.append({
                                            'name': name,
                                            'url': url,
                                            'logo': logo_url
                                        })
            except Exception as e:
                # print(f"Ошибка при разборе JSON __NEXT_DATA__: {e}")
                pass
                        
        except Exception as e:
            print(f"Ошибка при поиске watchability: {e}")
            
        return providers
    
    def _extract_from_meta(self) -> Dict:
        """Извлекает данные из JSON-LD метаданных."""
        result: Dict = {}
        try:
            for script in self.soup.find_all('script', type='application/ld+json'):
                raw = script.string or script.get_text()
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                except Exception:
                    continue
                nodes = data if isinstance(data, list) else [data]
                for node in nodes:
                    if not isinstance(node, dict):
                        continue
                    
                    # Определяем тип на основе URL
                    url_value = node.get('url')
                    if url_value:
                        url_str = str(url_value)
                        if '/series/' in url_str:
                            result['type'] = 'series'
                        elif '/film/' in url_str:
                            result['type'] = 'film'
                    
                    # Берём название фильма из name
                    name_value = node.get('name')
                    if name_value:
                        result['title'] = str(name_value)
                    
                    # Берём оригинальное название из alternateName
                    alternate_name = node.get('alternateName')
                    if alternate_name:
                        result['original_title'] = str(alternate_name)
                    
                    # Полное описание из description
                    description_value = node.get('description')
                    if description_value:
                        result['full_description'] = str(description_value)
                    
                    # Жанры из JSON-LD (строка или список)
                    genre_value = node.get('genre')
                    if genre_value:
                        if isinstance(genre_value, list):
                            result['genres'] = [str(g).strip() for g in genre_value if g]
                        else:
                            # Разбиваем строку по запятым/точкам с запятой
                            parts = [p.strip() for p in str(genre_value).replace(';', ',').split(',')]
                            result['genres'] = [p for p in parts if p]
                    
                    # Год выпуска (datePublished)
                    date_published = node.get('datePublished')
                    if date_published:
                        # Извлекаем только год, если дата в формате "2011-04-17"
                        date_str = str(date_published).strip()
                        year_match = re.search(r'(\d{4})', date_str)
                        if year_match:
                            result['year'] = year_match.group(1)
                        else:
                            result['year'] = date_str
                    
                    # Страны производства (countryOfOrigin)
                    countries_value = node.get('countryOfOrigin')
                    if countries_value:
                        if isinstance(countries_value, list):
                            result['countries'] = [str(c).strip() for c in countries_value if c]
                        else:
                            result['countries'] = [str(countries_value).strip()]
                    
                    # Семейный контент (isFamilyFriendly)
                    iff = node.get('isFamilyFriendly')
                    if iff is not None:
                        if isinstance(iff, bool):
                            result['isFamilyFriendly'] = iff
                        elif isinstance(iff, str):
                            # Если строка, преобразуем в bool
                            result['isFamilyFriendly'] = iff.lower() in ('true', '1', 'yes')
                    
                    # Количество серий (numberOfEpisodes)
                    number_of_episodes = node.get('numberOfEpisodes')
                    if number_of_episodes is not None:
                        result['numberOfEpisodes'] = int(number_of_episodes) if isinstance(number_of_episodes, (int, str)) and str(number_of_episodes).isdigit() else str(number_of_episodes)
                    
                    # Возрастной рейтинг (contentRating)
                    content_rating = node.get('contentRating')
                    if content_rating:
                        result['content_rating'] = str(content_rating)
                    
                    return result
        except Exception:
            pass
        return result

    def _normalize_url(self, url: str) -> str:
        """Нормализует URL, добавляя протокол если нужно"""
        if not url:
            return url
        if url.startswith('//'):
            return 'https:' + url
        if not url.startswith('http'):
            return 'https://' + url
        return url

    
    def save_to_json(self, film_data: Dict, output_file: str = 'output/film_details.json'):
        """Сохраняет данные о фильме в JSON файл"""
        super().save_to_json(film_data, output_file)
    
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
        if film_data.get('age_rating'):
            print(f"🔞 Возрастной рейтинг: {film_data['age_rating']}")
        
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
    parser = SerialPageParser()
    
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
