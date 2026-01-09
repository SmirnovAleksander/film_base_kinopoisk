#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Общий файл запуска парсеров Кинопоиска
Позволяет выбрать нужный вариант парсинга из меню
"""

import sys
import os
import json
from datetime import datetime

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
    print("  5. Парсер новостей (локальный)")
    print("  6. Парсер страницы сериала (локальный)")
    
    print("\n🌐 ОНЛАЙН ПАРСЕРЫ (с сайта):")
    print("  7. Парсер всех фильмов (онлайн)")
    print("  8. Парсер страницы фильма (онлайн)")
    print("  9. Парсер страницы актера (онлайн)")
    print(" 10. Парсер галереи кадров (онлайн)")
    print(" 11. Парсер новостей (онлайн)")
    print(" 12. Парсер страницы сериала (онлайн)")
    
    print("\n⚙️  СПЕЦИАЛЬНЫЕ ПАРСЕРЫ:")
    print(" 13. Главный парсер фильмов")
    print(" 14. Главный парсер сериалов")
    print(" 15. Главный парсер фильмов и сериалов")
    print(" 16. Парсер всех типов медиа контента")
    
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
            output_file = 'output/film_details.json'
            parser.save_to_json(film_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация о фильме не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        

def run_serial_parser_local():
    """Парсер страницы сериала (локальный)"""
    from parser_utils.serial_page_parser import SerialPageParser
    
    print("\n=== Парсер страницы сериала (локальный) ===")
    
    html_file = 'templates/serial_page_kinopoisk.html'
    if not os.path.exists(html_file):
        # Если нет специального файла для сериала, пробуем обычный файл фильма
        html_file = 'templates/film_page_kinopoisk.html'
        
    if not os.path.exists(html_file):
        print(f"❌ Ошибка: Файл {html_file} не найден!")
        return
    
    try:
        parser = SerialPageParser()
        print(f"Загружаем HTML файл {html_file}...")
        parser.load_html_from_file(html_file)
        print("✓ HTML файл загружен")
        
        print("Извлекаем детальную информацию о сериале...")
        serial_data = parser.extract_film_details()
        print("✓ Информация извлечена")
        
        if serial_data:
            output_file = 'output/serial_details.json'
            parser.save_to_json(serial_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация о сериале не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_actor_parser_local():
    """Парсер страницы актера (локальный)"""
    from parser_utils.stuff_page_parser import ActorPageParser
    
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
            output_file = 'output/stuff_details.json'
            parser.save_to_json(actor_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация об актере не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

def run_news_parser_local():
    """Парсер новостей (локальный)"""
    from parser_utils.news_page_parser import NewsPageParser
    
    print("\n=== Парсер новостей (локальный) ===")
    
    html_file = "templates/news_page.html"
    if not os.path.exists(html_file):
        print(f"❌ HTML файл не найден: {html_file}")
        return
    
    try:
        parser = NewsPageParser()
        parser.load_html_from_file(html_file)
        
        if parser.soup:
            news_list = parser.parse_news_list()
            result = {
                'news_list': news_list,
                'parsed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source_file': html_file,
                'total_news': len(news_list)
            }
            filename = "output/news_local.json"
            parser.save_to_json(result, filename)
            print(f"✅ Найдено новостей: {len(news_list)}. Файл: {filename}")
        else:
            print("❌ Не удалось загрузить HTML файл")
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
            
            print(f"\n=== Статистика ===")
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
    
    film_url = "https://www.kinopoisk.ru/film/1143242/"  # Джентельмены
    
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
            output_file = 'output/online_film_details.json'
            parser.save_to_json(film_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация о фильме не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_serial_parser_online():
    """Парсер страницы сериала (онлайн)"""
    from parser_utils.serial_page_parser import SerialPageParser
    
    print("\n=== Парсер страницы сериала (онлайн) ===")
    
    serial_url = "https://www.kinopoisk.ru/series/796660/"  # Лучше звоните Солу
    
    try:
        parser = SerialPageParser()
        print(f"Загружаем данные с {serial_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(serial_url)
        print("✓ HTML загружен с сайта")
        
        print("Извлекаем детальную информацию о сериале...")
        serial_data = parser.extract_film_details()
        print("✓ Информация извлечена")
        
        if serial_data:
            output_file = 'output/online_serial_details.json'
            parser.save_to_json(serial_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация о сериале не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_actor_parser_online():
    """Парсер страницы актера (онлайн)"""
    from parser_utils.stuff_page_parser import ActorPageParser
    
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
            output_file = 'output/online_stuff_details.json'
            parser.save_to_json(actor_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
        else:
            print("⚠️ Информация об актере не найдена.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_stills_parser_online():
    """Парсер галереи кадров (онлайн) - использует новый GraphQL парсер"""
    from parser_utils.film_series_images_parser import FilmImagesParser
    import json
    import os
    
    print("\n=== Парсер галереи кадров (онлайн - GraphQL) ===")
    
    # Для онлайн тестирования используем пример ID фильма
    test_movie_id = "258687"  # Пример ID фильма
    try:
        parser = FilmImagesParser()
        print(f"Получение изображений для фильма {test_movie_id} через GraphQL API...")
        
        # Получаем все типы изображений
        all_images = parser.fetch_all_image_types(test_movie_id)
        
        os.makedirs('output', exist_ok=True)
        out_all = 'output/stills_online.json'
        with open(out_all, 'w', encoding='utf-8') as f:
            json.dump(all_images, f, ensure_ascii=False, indent=2)
        print(f"✅ Найдено изображений: {len(all_images)}. Файл: {out_all}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_news_parser_online():
    """Парсер новостей (онлайн)"""
    from parser_utils.news_page_parser import NewsPageParser
    
    print("\n=== Парсер новостей (онлайн) ===")
    
    news_url = "https://www.kinopoisk.ru/media/"
    
    try:
        parser = NewsPageParser()
        print("Парсим новости с 5 страниц...")
        news_list = parser.parse_multiple_pages(5)
        
        if news_list:
            result = {
                'news_list': news_list,
                'parsed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source_url': news_url,
                'total_news': len(news_list)
            }
            filename = "output/news_online.json"
            parser.save_to_json(result, filename)
            print(f"✅ Найдено новостей: {len(news_list)}. Файл: {filename}")
        else:
            print("❌ Не удалось загрузить страницу")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


def run_main_parser_films():
    """Главный парсер только фильмов"""
    from main_parser import MainParser
    
    print("\n🚀 Запуск главного парсера фильмов Кинопоиска")
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


def run_main_parser_series():
    """Главный парсер только сериалов"""
    from main_parser import MainParser
    
    print("\n🚀 Запуск главного парсера сериалов Кинопоиска")
    print("=" * 50)
    
    try:
        parser = MainParser()
        from config import PARSING_CONFIG
        parser.parse_all_series(start_page=PARSING_CONFIG['START_PAGE'], max_pages=PARSING_CONFIG['MAX_PAGES'])
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 Парсинг завершен")


def run_main_parser_all():
    """Главный парсер фильмов и сериалов"""
    from main_parser import MainParser
    
    print("\n🚀 Запуск главного парсера фильмов и сериалов Кинопоиска")
    print("=" * 50)
    
    try:
        parser = MainParser()
        from config import PARSING_CONFIG
        # Сначала парсим сериалы
        parser.parse_all_series(start_page=PARSING_CONFIG['START_PAGE'], max_pages=PARSING_CONFIG['MAX_PAGES'])
        # Затем парсим фильмы
        parser.parse_all_films(start_page=PARSING_CONFIG['START_PAGE'], max_pages=PARSING_CONFIG['MAX_PAGES'])
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 Парсинг завершен")


def run_all_media_parser():
    """Парсер всех типов медиа контента"""
    from parser_utils.news_page_parser import NewsPageParser
    from main_parser import MainParser
    
    print("\n🚀 Запуск парсера всех типов медиа контента")
    
    os.makedirs("output", exist_ok=True)
    
    parser = NewsPageParser()
    main_parser = MainParser()
    
    content_types = ['media', 'news', 'article']
    all_content = []
    
    try:
        for content_type in content_types:
            print(f"\n📺 Парсинг {content_type}...")
            content = parser.parse_multiple_pages(pages_count=2, content_type=content_type)
            
            if content:
                all_content.extend(content)
                print(f"✅ {content_type}: найдено {len(content)} элементов")
            else:
                print(f"❌ {content_type}: не найдено элементов")
        
        if all_content:
            output_file = "output/all_media.json"
            parser.save_to_json(all_content, output_file)
            print(f"\n💾 Сохранено в {output_file}")
            
            print("💾 Сохранение в базу данных...")
            main_parser.save_media_to_db(all_content)
            
            print(f"\n📊 Итого найдено: {len(all_content)} элементов")
            
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
        import traceback
        traceback.print_exc()


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
            elif choice == '5':
                run_news_parser_local()
            elif choice == '6':
                run_serial_parser_local()
            elif choice == '7':
                run_parser_online()
            elif choice == '8':
                run_film_parser_online()
            elif choice == '9':
                run_actor_parser_online()
            elif choice == '10':
                run_stills_parser_online()
            elif choice == '11':
                run_news_parser_online()
            elif choice == '12':
                run_serial_parser_online()
            elif choice == '13':
                run_main_parser_films()
            elif choice == '14':
                run_main_parser_series()
            elif choice == '15':
                run_main_parser_all()
            elif choice == '16':
                run_all_media_parser()
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

