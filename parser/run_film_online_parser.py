#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга страницы отдельного фильма (онлайн)
"""

import sys
import os
from parser_utils.film_page_parser import FilmPageParser


def main():
    """Основная функция"""
    print("=== Парсер страницы фильма (онлайн) ===")
    print()
    
    # URL для парсинга (можно изменить на нужный фильм)
    film_url = "https://www.kinopoisk.ru/film/689/"  # 1+1
    
    try:
        # Создаем парсер
        parser = FilmPageParser()
        
        # Загружаем HTML с сайта
        print(f"Загружаем данные с {film_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(film_url)
        print("✓ HTML загружен с сайта")
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию о фильме...")
        film_data = parser.extract_film_details()
        print("✓ Информация извлечена")
        
        # Выводим результаты
        if film_data:
            parser.print_film_details(film_data)
            
            # Сохраняем в JSON
            output_file = 'output/online_film_details.json'
            parser.save_to_json(film_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
        else:
            print("⚠️ Информация о фильме не найдена.")
            print("Возможные причины:")
            print("1. Сайт заблокировал запрос (защита от ботов)")
            print("2. Изменилась структура страницы")
            print("3. Нет интернет-соединения")
            print("\nПопробуйте:")
            print("- Запустить скрипт позже")
            print("- Использовать VPN")
            print("- Использовать локальный HTML файл (run_film_parser.py)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\nВозможные решения:")
        print("1. Проверьте интернет-соединение")
        print("2. Попробуйте использовать VPN")
        print("3. Запустите скрипт позже")
        print("4. Используйте локальный HTML файл")
        
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
