#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Общий файл запуска парсеров Кинопоиска
Позволяет выбрать нужный вариант парсинга из меню
"""

import sys
import os
import json

# Добавляем путь к модулям парсера
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def print_menu():
    """Выводит меню выбора парсера"""
    print("\n" + "=" * 60)
    print("🚀 ПАРСЕРЫ КИНОПОИСКА")
    print("=" * 60)
    print("\n📋 Выберите вариант парсинга:\n")
    
    print("📁 ЛОКАЛЬНЫЕ ПАРСЕРЫ (из HTML файлов):")
    print("  1. Парсер всех фильмов (локальный)")
    print("  2. Парсер страницы фильма (локальный)")
    print("  3. Парсер страницы актера (локальный)")
    print("  4. Парсер галереи кадров (локальный)")
    
    print("\n🌐 ОНЛАЙН ПАРСЕРЫ (с сайта):")
    print("  6. Парсер всех фильмов (онлайн)")
    print("  7. Парсер страницы фильма (онлайн)")
    print("  8. Парсер страницы актера (онлайн)")
    print("  9. Парсер галереи кадров (онлайн)")
    
    print("\n⚙️  СПЕЦИАЛЬНЫЕ ПАРСЕРЫ:")
    print(" 11. Главный парсер фильмов и актеров")
    
    print("\n  0. Выход")
    print("=" * 60)


def run_parser_local():
    """Парсер всех фильмов (локальный)"""
    from parser_utils.kinopoisk_parser import KinopoiskParser
    
    print("\n=== Парсер Кинопоиска (локальный) ===")
    
    html_file = 'templates/all_films_kinopoisk.html'
    if not os.path.exists(html_file):
        print(f"❌ Ошибка: Файл {html_file} не найден!")
        print("Убедитесь, что HTML файл находится в папке templates/")
        return
    
    try:
        parser = KinopoiskParser()
        print("Загружаем HTML файл...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        print("Парсим данные о фильмах...")
        films = parser.parse_all_films()
        print(f"✓ Найдено фильмов: {len(films)}")
        
        if films:
            print("\n=== Результаты парсинга ===")
            parser.print_films_summary(films)
            
            output_file = 'output/parsed_films.json'
            parser.save_to_json(films, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠ Фильмы не найдены.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_film_parser_local():
    """Парсер страницы фильма (локальный)"""
    from parser_utils.film_page_parser import FilmPageParser
    
    print("\n=== Парсер страницы фильма (локальный) ===")
    
    html_file = 'templates/film_page_kinopoisk.html'
    if not os.path.exists(html_file):
        print(f"❌ Ошибка: Файл {html_file} не найден!")
        return
    
    try:
        parser = FilmPageParser()
        print("Загружаем HTML файл...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        print("Извлекаем детальную информацию о фильме...")
        film_data = parser.extract_film_details()
        print("✓ Информация извлечена")
        
        if film_data:
            parser.print_film_details(film_data)
            output_file = 'output/film_details.json'
            parser.save_to_json(film_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация о фильме не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_actor_parser_local():
    """Парсер страницы актера (локальный)"""
    from parser_utils.actor_page_parser import ActorPageParser
    
    print("\n=== Парсер страницы актера (локальный) ===")
    
    html_file = 'templates/actor_page_kinopoisk.html'
    if not os.path.exists(html_file):
        print(f"❌ Ошибка: Файл {html_file} не найден!")
        return
    
    try:
        parser = ActorPageParser()
        print("Загружаем HTML файл...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        print("Извлекаем детальную информацию об актере...")
        actor_data = parser.extract_actor_details()
        print("✓ Информация извлечена")
        
        if actor_data:
            parser.print_actor_details(actor_data)
            output_file = 'output/actor_details.json'
            parser.save_to_json(actor_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация об актере не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_stills_parser_local():
    """Парсер галереи кадров (локальный)"""
    from parser_utils.stills_page_parser import StillsPageParser
    
    print("\n=== Парсер галереи кадров (локальный) ===")
    
    html_file = 'templates/posters_page.html'
    try:
        parser = StillsPageParser()
        parser.load_html_from_file(html_file)
        items = parser.extract_stills_info()
        os.makedirs('output', exist_ok=True)
        out_all = 'output/stills_local.json'
        with open(out_all, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✅ Найдено карточек: {len(items)}. Файл: {out_all}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

def run_parser_online():
    """Парсер всех фильмов (онлайн)"""
    from parser_utils.kinopoisk_parser import KinopoiskParser
    
    print("\n=== Онлайн парсер Кинопоиска ===")
    
    kinopoisk_url = "https://www.kinopoisk.ru/lists/movies/?b=films&b=high_rated"
    
    try:
        parser = KinopoiskParser()
        print(f"Загружаем данные с {kinopoisk_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(kinopoisk_url)
        print("✓ HTML загружен с сайта")
        
        print("Парсим данные о фильмах...")
        films = parser.parse_all_films()
        print(f"✓ Найдено фильмов: {len(films)}")
        
        if films:
            print("\n=== Результаты парсинга ===")
            parser.print_films_summary(films)
            
            output_file = 'output/online_parsed_films.json'
            parser.save_to_json(films, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
            print("\n=== Статистика ===")
            print(f"Всего фильмов: {len(films)}")
            films_with_rating = [f for f in films if f.get('rating') and f['rating'] != 'Неизвестно']
            print(f"Фильмов с рейтингом: {len(films_with_rating)}")
        else:
            print("⚠️ Фильмы не найдены.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("\nВозможные решения:")
        print("1. Проверьте интернет-соединение")
        print("2. Попробуйте использовать VPN")
        print("3. Запустите скрипт позже")
        import traceback
        traceback.print_exc()


def run_film_parser_online():
    """Парсер страницы фильма (онлайн)"""
    from parser_utils.film_page_parser import FilmPageParser
    
    print("\n=== Парсер страницы фильма (онлайн) ===")
    
    film_url = "https://www.kinopoisk.ru/film/535341/"  # 1+1
    
    try:
        parser = FilmPageParser()
        print(f"Загружаем данные с {film_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(film_url)
        print("✓ HTML загружен с сайта")
        
        print("Извлекаем детальную информацию о фильме...")
        film_data = parser.extract_film_details()
        print("✓ Информация извлечена")
        
        if film_data:
            parser.print_film_details(film_data)
            output_file = 'output/online_film_details.json'
            parser.save_to_json(film_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация о фильме не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_actor_parser_online():
    """Парсер страницы актера (онлайн)"""
    from parser_utils.actor_page_parser import ActorPageParser
    
    print("\n=== Парсер страницы актера (онлайн) ===")
    
    actor_url = "https://www.kinopoisk.ru/name/41644/"  # Омар Си
    
    try:
        parser = ActorPageParser()
        print(f"Загружаем данные с {actor_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(actor_url)
        print("✓ HTML загружен с сайта")
        
        print("Извлекаем детальную информацию об актере...")
        actor_data = parser.extract_actor_details()
        print("✓ Информация извлечена")
        
        if actor_data:
            parser.print_actor_details(actor_data)
            output_file = 'output/online_actor_details.json'
            parser.save_to_json(actor_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация об актере не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_stills_parser_online():
    """Парсер галереи кадров (онлайн)"""
    from parser_utils.stills_page_parser import StillsPageParser
    
    print("\n=== Парсер галереи кадров (онлайн) ===")
    
    urls = [
        'https://www.kinopoisk.ru/film/535341/stills/',
        'https://www.kinopoisk.ru/film/535341/wall/',
    ]
    
    try:
        parser = StillsPageParser()
        grouped = {"stills": [], "wall": []}
        for url in urls:
            try:
                parser.load_html_from_url(url)
                items = parser.extract_stills_info()
                key = 'stills' if '/stills' in url else ('wall' if '/wall' in url else 'stills')
                grouped[key].extend(items)
            except Exception as e:
                print(f"⚠️ Пропущен URL {url}: {e}")
        
        os.makedirs('output', exist_ok=True)
        out_all = 'output/stills_online.json'
        with open(out_all, 'w', encoding='utf-8') as f:
            json.dump(grouped, f, ensure_ascii=False, indent=2)
        print(f"✅ Найдено карточек: stills={len(grouped['stills'])}, wall={len(grouped['wall'])}. Файл: {out_all}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

def run_main_parser():
    """Главный парсер фильмов и актеров"""
    from main_parser import MainParser
    
    print("\n🚀 Запуск главного парсера Кинопоиска")
    print("=" * 50)
    
    try:
        parser = MainParser()
        from config import PARSING_CONFIG
        parser.parse_all_films(start_page=PARSING_CONFIG['START_PAGE'], max_pages=PARSING_CONFIG['MAX_PAGES'])
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 Парсинг завершен")

def main():
    """Главная функция"""
    while True:
        print_menu()
        
        try:
            choice = input("\n👉 Ваш выбор: ").strip()
            
            if choice == '0':
                print("\n👋 До свидания!")
                break
            elif choice == '1':
                run_parser_local()
            elif choice == '2':
                run_film_parser_local()
            elif choice == '3':
                run_actor_parser_local()
            elif choice == '4':
                run_stills_parser_local()
            elif choice == '6':
                run_parser_online()
            elif choice == '7':
                run_film_parser_online()
            elif choice == '8':
                run_actor_parser_online()
            elif choice == '9':
                run_stills_parser_online()
            elif choice == '11':
                run_main_parser()
            else:
                print("\n❌ Неверный выбор! Попробуйте снова.")
                continue
            
            input("\n⏸️  Нажмите Enter для продолжения...")
            
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            input("\n⏸️  Нажмите Enter для продолжения...")


if __name__ == "__main__":
    main()

