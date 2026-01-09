#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения изображений фильма через GraphQL API Кинопоиска
"""

import requests
import json
from parser_utils.base_parser import BaseParser


class FilmImagesParser(BaseParser):
    """Класс для получения изображений фильма через GraphQL API"""

    def __init__(self):
        super().__init__()
        self.graphql_url = "https://graphql.kinopoisk.ru/graphql/"
        
    def _prepare_session(self):
        """Подготовка сессии с правильными заголовками"""
        # Используем тот же подход, что и в base_parser
        session = requests.Session()
        
        # Устанавливаем заголовки как в base_parser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.kinopoisk.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Service-Id': '25',
            'X-Preferred-Language': 'ru',
            'Priority': 'u=1, i'
        }
        session.headers.update(headers)
        
        # Загружаем cookies если есть
        self._load_cookies(session)
        
        # Устанавливаем Content-Type для GraphQL
        session.headers.update({
            'Content-Type': 'application/json'
        })
        return session
        
    def fetch_movie_images_paginated(self, movie_id: int, image_type: str = "STILL", limit: int = 42):
        """
        Получает все изображения фильма через GraphQL API с пагинацией
        
        Args:
            movie_id: ID фильма
            image_type: Тип изображений (STILL, POSTER, SHOOTING, WALL, SCREENSHOT)
            limit: Количество изображений для получения на одной странице
        """
        # GraphQL запрос
        query = """
query MovieImagesItems($id: Long!, $type: MovieImageType!, $offset: Int, $limit: Int) {
   movie(id: $id) {
       id
       ...MovieImages
       __typename
   }
}
fragment MovieImages on Movie {
   images(types: [$type], offset: $offset, limit: $limit) {
       items {
           id
           type
           image {
               avatarsUrl
               origSize {
                   width
                   height
                   __typename
               }
               __typename
           }
           __typename
       }
       total
       __typename
   }
   __typename
}
"""

        all_images_structured = []
        offset = 0
        total_images = 0
        
        # Подготовка сессии - используем тот же подход, что и в base_parser
        session = self._prepare_session()
        
        # Добавляем параметры к URL
        url_with_params = f"{self.graphql_url}?operationName=MovieImagesItems"
        
        try:
            while True:
                variables = {
                    "id": movie_id,
                    "type": image_type,
                    "offset": offset,
                    "limit": limit
                }

                payload = {
                    "operationName": "MovieImagesItems",
                    "query": query,
                    "variables": variables
                }
                
                response = session.post(
                    url_with_params,
                    json=payload,
                    timeout=30
                )
                
                response.raise_for_status()
                
                result = response.json()
                
                # Если есть изображения, выводим их количество
                if 'data' in result and 'movie' in result['data']:
                    images_data = result['data']['movie'].get('images', {})
                    total = images_data.get('total', 0)
                    items = images_data.get('items', [])
                    
                    # Если нет изображений на этой странице, завершаем цикл
                    if not items:
                        print("Больше изображений нет (пустая страница)")
                        break
                    
                    # Обновляем общее количество изображений
                    if total > total_images:
                        total_images = total
                   
                    # Преобразуем изображения в структурированный формат
                    for item in items:
                        img_info = item.get('image', {})
                        orig_size = img_info.get('origSize', {})
                        
                        # Нормализуем URL изображения
                        original_url = img_info.get('avatarsUrl')
                        if original_url:
                            normalized_url = self._normalize_url(original_url)
                        else:
                            normalized_url = None
                        
                        # Создаем структурированный словарь в формате, аналогичном stills_page_parser.py
                        structured_item = {
                            'id': item.get('id'),
                            'original': normalized_url,  # Используем нормализованный URL как оригинальное изображение
                            'type': image_type.lower()  # Приводим к нижнему регистру для соответствия
                        }
                        
                        all_images_structured.append(structured_item)
                          
                    # Проверяем, получили ли мы все изображения
                    if len(all_images_structured) >= total:
                        break
                    
                    # Увеличиваем offset для следующего запроса
                    offset += limit
                else:
                    print("Нет данных в ответе от API")
                    break
            
            return all_images_structured
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            if hasattr(e.response, 'text') and e.response.text:
                print(f"Тело ответа ошибки: {e.response.text}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None
    
    def fetch_all_image_types(self, movie_id: int, limit: int = 42):
        """
        Получает все изображения фильма для всех типов: STILL, SHOOTING, POSTER
        
        Args:
            movie_id: ID фильма
            limit: Количество изображений для получения на одной странице
        """
        image_types = ["STILL", "SHOOTING", "POSTER"]
        all_results = {}
        
        # Структурированные данные для всех типов
        all_structured_data = []
        
        for image_type in image_types:       
            images = self.fetch_movie_images_paginated(movie_id, image_type, limit)
            all_results[image_type] = images
            
            if images is not None:
                # Добавляем данные в общий список с типом
                for item in images:
                    item_with_type = item.copy()  # Создаем копию
                    # Нормализуем URL изображения
                    if item_with_type.get('original'):
                        item_with_type['original'] = self._normalize_url(item_with_type['original'])
                    item_with_type['type'] = image_type.lower()  # Добавляем тип
                    all_structured_data.append(item_with_type)
            else:
                print(f"\nОшибка при получении изображений типа {image_type}")
        
        # Возвращаем структурированные данные в формате, аналогичном stills_page_parser.py
        return all_structured_data


def main():
    """Основная функция"""
    fetcher = FilmImagesParser()
    
    # Пример использования
    movie_id = 258687  # ID фильма (как в примере из задачи)
    limit = 42  # Лимит
    
    # Получаем все изображения в структурированном формате
    all_images = fetcher.fetch_all_image_types(movie_id, limit)
      
    # Считаем по типам
    type_counts = {}
    total_count = len(all_images)
    
    # Проходим по каждому изображению и группируем по типу
    for item in all_images:
        image_type = item.get('type', 'unknown')
        type_counts[image_type] = type_counts.get(image_type, 0) + 1
    
    for image_type, count in type_counts.items():
        print(f"{image_type.upper()}: {count} изображений")
    
    print(f"Всего изображений: {total_count}")


if __name__ == "__main__":
    main()
