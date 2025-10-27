#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга Кинопоиска напрямую с сайта
"""

import sys
import os
from parser_utils.kinopoisk_parser import KinopoiskParser


def main():
    """Основная функция"""
    print("=== Онлайн парсер Кинопоиска ===")
    print()
    
    # URL для парсинга
    kinopoisk_url = "https://www.kinopoisk.ru/lists/movies/?b=films&b=high_rated"
    
    try:
        # Создаем парсер
        parser = KinopoiskParser()
        
        # Загружаем HTML с сайта
        print(f"Загружаем данные с {kinopoisk_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(kinopoisk_url)
        print("✓ HTML загружен с сайта")
        
        # Парсим фильмы
        print("Парсим данные о фильмах...")
        films = parser.parse_all_films()
        print(f"✓ Найдено фильмов: {len(films)}")
        
        # Выводим результаты
        if films:
            print("\n=== Результаты парсинга ===")
            parser.print_films_summary(films)
            
            # Сохраняем в JSON
            output_file = 'output/online_parsed_films.json'
            parser.save_to_json(films, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
            # Показываем статистику
            print(f"\n=== Статистика ===")
            print(f"Всего фильмов: {len(films)}")
            
            # Фильмы с рейтингом
            films_with_rating = [f for f in films if f.get('rating') and f['rating'] != 'Неизвестно']
            print(f"Фильмов с рейтингом: {len(films_with_rating)}")
            
            # Фильмы с жанрами
            films_with_genres = [f for f in films if f.get('genres')]
            print(f"Фильмов с жанрами: {len(films_with_genres)}")
            
            # Топ-5 фильмов по рейтингу
            if films_with_rating:
                print(f"\n=== Топ-5 фильмов по рейтингу ===")
                sorted_films = sorted(films_with_rating, 
                                    key=lambda x: float(x['rating']) if x['rating'].replace('.', '').isdigit() else 0, 
                                    reverse=True)
                for i, film in enumerate(sorted_films[:5], 1):
                    print(f"{i}. {film['title']} ({film.get('year', 'Неизвестно')}) - {film['rating']}")
            
        else:
            print("⚠️ Фильмы не найдены.")
            print("Возможные причины:")
            print("1. Сайт заблокировал запрос (защита от ботов)")
            print("2. Изменилась структура страницы")
            print("3. Нет интернет-соединения")
            print("\nПопробуйте:")
            print("- Запустить скрипт позже")
            print("- Использовать VPN")
            print("- Использовать локальный HTML файл (run_parser.py)")
        
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
