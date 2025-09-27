#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга страницы актера (локальный HTML)
"""

import sys
import os
from parser.actor_page_parser import ActorPageParser


def main():
    """Основная функция"""
    print("=== Парсер страницы актера (локальный) ===")
    print()
    
    # Проверяем наличие HTML файла
    html_file = 'templates/actor_page_kinopoisk.html'
    if not os.path.exists(html_file):
        print(f"Ошибка: Файл {html_file} не найден!")
        print("Убедитесь, что HTML файл находится в папке templates/")
        return
    
    try:
        # Создаем парсер
        parser = ActorPageParser()
        
        # Загружаем HTML
        print("Загружаем HTML файл...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию об актере...")
        actor_data = parser.extract_actor_details()
        print("✓ Информация извлечена")
        
        # Выводим результаты
        if actor_data:
            parser.print_actor_details(actor_data)
            
            # Сохраняем в JSON
            output_file = 'output/actor_details.json'
            parser.save_to_json(actor_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
        else:
            print("⚠️ Информация об актере не найдена.")
            print("Возможно, структура HTML изменилась.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
