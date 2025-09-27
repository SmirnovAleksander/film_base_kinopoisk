#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга страницы отдельного фильма (локальный HTML)
"""

import sys
import os
from parser.film_page_parser import FilmPageParser


def main():
    """Основная функция"""
    print("=== Парсер страницы фильма (локальный) ===")
    print()
    
    # Проверяем наличие HTML файла
    html_file = 'templates/film_page_kinopoisk.html'
    if not os.path.exists(html_file):
        print(f"Ошибка: Файл {html_file} не найден!")
        print("Убедитесь, что HTML файл находится в папке templates/")
        return
    
    try:
        # Создаем парсер
        parser = FilmPageParser()
        
        # Загружаем HTML
        print("Загружаем HTML файл...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию о фильме...")
        film_data = parser.extract_film_details()
        print("✓ Информация извлечена")
        
        # Выводим результаты
        if film_data:
            parser.print_film_details(film_data)
            
            # Сохраняем в JSON
            output_file = 'output/film_details.json'
            parser.save_to_json(film_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
        else:
            print("⚠️ Информация о фильме не найдена.")
            print("Возможно, структура HTML изменилась.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
