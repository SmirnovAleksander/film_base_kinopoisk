#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга допустимых типов медиа контента Кинопоиска
Парсит только: media (лендинг), news, article — по 2 страницы каждый
"""

import json
import os
from parser.news_page_parser import NewsPageParser
from main_parser import MainParser

def main():
    """Основная функция"""
    print("🚀 Запуск парсера всех типов медиа контента")
    
    # Создаем папку output если её нет
    os.makedirs("output", exist_ok=True)
    
    # Инициализируем парсер
    parser = NewsPageParser()
    main_parser = MainParser()
    
    # Допустимые типы контента
    content_types = ['media', 'news', 'article']
    all_content = []
    
    try:
        # Парсим каждый тип контента по 2 страницы
        for content_type in content_types:
            print(f"\n📺 Парсинг {content_type}...")
            
            # Парсим 2 страницы для каждого типа
            content = parser.parse_multiple_pages(pages_count=2, content_type=content_type)
            
            if content:
                all_content.extend(content)
                print(f"✅ {content_type}: найдено {len(content)} элементов")
            else:
                print(f"❌ {content_type}: не найдено элементов")
        
        # Сохраняем в JSON
        if all_content:
            output_file = "output/all_media.json"
            parser.save_to_json(all_content, output_file)
            print(f"\n💾 Сохранено в {output_file}")
            
            # Сохраняем в БД
            print("💾 Сохранение в базу данных...")
            main_parser.save_media_to_db(all_content)
            
            # Статистика
            print(f"\n📊 Итого найдено: {len(all_content)} элементов")
            
            # Статистика по типам
            type_stats = {}
            for item in all_content:
                content_type = item.get('type', 'unknown')
                type_stats[content_type] = type_stats.get(content_type, 0) + 1
            
            print("📈 Статистика по типам:")
            for content_type, count in type_stats.items():
                print(f"  - {content_type}: {count} элементов")
                
        else:
            print("❌ Не найдено контента для сохранения")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
