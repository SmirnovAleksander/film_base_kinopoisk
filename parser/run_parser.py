#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска парсера Кинопоиска
"""

import sys
import os
from parser_utils.kinopoisk_parser import KinopoiskParser


def main():
    """Основная функция"""
    print("=== Парсер Кинопоиска ===")
    print()
    
    # Проверяем наличие HTML файла
    html_file = 'templates/all_films_kinopoisk.html'
    if not os.path.exists(html_file):
        print(f"Ошибка: Файл {html_file} не найден!")
        print("Убедитесь, что HTML файл находится в папке templates/")
        return
    
    try:
        # Создаем парсер
        parser = KinopoiskParser()
        
        # Загружаем HTML
        print("Загружаем HTML файл...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        # Парсим фильмы
        print("Парсим данные о фильмах...")
        films = parser.parse_all_films()
        print(f"✓ Найдено фильмов: {len(films)}")
        
        # Выводим результаты
        if films:
            print("\n=== Результаты парсинга ===")
            parser.print_films_summary(films)
            
            # Сохраняем в JSON
            output_file = 'output/parsed_films.json'
            parser.save_to_json(films, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
        else:
            print("⚠ Фильмы не найдены. Возможно, структура HTML изменилась.")
            print("Попробуйте обновить HTML файл или проверить селекторы в коде.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
