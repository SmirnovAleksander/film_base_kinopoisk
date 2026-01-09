#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения изображений персоны через GraphQL API Кинопоиска
"""

import requests
from parser_utils.base_parser import BaseParser


class StuffImagesParser(BaseParser):
    """Класс для получения изображений персоны через GraphQL API"""

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
        
    def fetch_stuff_images_paginated(self, stuff_id: int, image_type: str = "PHOTO", limit: int = 42):
        """
        Получает все изображения персоны через GraphQL API с пагинацией
        
        Args:
            stuff_id: ID персоны
            image_type: Тип изображений (PHOTO)
            limit: Количество изображений для получения на одной странице
        """
        # GraphQL запрос
        query = """
                query PersonImagesItems($id: Long!, $type: PersonImageType!, $offset: Int, $limit: Int) {
                person(id: $id) {
                    id
                    ...PersonImages
                    __typename
                }
                }
                fragment PersonImages on Person {
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
        
        # Подготовка сессии
        session = self._prepare_session()
        
        # Добавляем параметры к URL
        url_with_params = f"{self.graphql_url}?operationName=PersonImagesItems"
        
        try:
            while True:
                variables = {
                    "id": stuff_id,
                    "type": image_type,
                    "offset": offset,
                    "limit": limit
                }

                payload = {
                    "operationName": "PersonImagesItems",
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
                if 'data' in result and 'person' in result['data']:
                    images_data = result['data']['person'].get('images', {})
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
                        
                        # Нормализуем URL изображения
                        original_url = img_info.get('avatarsUrl')
                        if original_url:
                            normalized_url = self._normalize_url(original_url)
                        else:
                            normalized_url = None
                        
                        # Создаем структурированный словарь
                        structured_item = {
                            'id': item.get('id'),
                            'original': normalized_url,
                            'type': image_type.lower()
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
    
    def fetch_all_image_types(self, stuff_id: int, limit: int = 42):
        """
        Получает все изображения персоны для всех типов: PHOTO
        
        Args:
            stuff_id: ID персоны
            limit: Количество изображений для получения на одной странице
        """
        image_types = ["PHOTO"]
        all_results = {}
        
        # Структурированные данные для всех типов
        all_structured_data = []
        
        for image_type in image_types:       
            images = self.fetch_stuff_images_paginated(stuff_id, image_type, limit)
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
        
        return all_structured_data


def main():
    """Основная функция"""
    fetcher = StuffImagesParser()
    
    # Пример использования
    stuff_id = 12345  # Пример ID
    limit = 42
    
    # Получаем все изображения в структурированном формате
    all_images = fetcher.fetch_all_image_types(stuff_id, limit)
      
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