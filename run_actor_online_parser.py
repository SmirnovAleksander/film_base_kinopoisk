#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга страницы актера (онлайн)
"""

import sys
import os
from parser.actor_page_parser import ActorPageParser


def main():
    """Основная функция"""
    print("=== Парсер страницы актера (онлайн) ===")
    print()
    
    # URL для парсинга (можно изменить на нужного актера)
    actor_url = "https://www.kinopoisk.ru/name/41644/"  # Омар Си
    
    try:
        # Создаем парсер
        parser = ActorPageParser()
        
        # Загружаем HTML с сайта
        print(f"Загружаем данные с {actor_url}...")
        print("⚠️ Это может занять некоторое время из-за защиты от ботов...")
        
        parser.load_html_from_url(actor_url)
        print("✓ HTML загружен с сайта")
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию об актере...")
        actor_data = parser.extract_actor_details()
        print("✓ Информация извлечена")
        
        # Выводим результаты
        if actor_data:
            parser.print_actor_details(actor_data)
            
            # Сохраняем в JSON
            output_file = 'output/online_actor_details.json'
            parser.save_to_json(actor_data, output_file)
            print(f"✓ Данные сохранены в {output_file}")
            
        else:
            print("⚠️ Информация об актере не найдена.")
            print("Возможные причины:")
            print("1. Сайт заблокировал запрос (защита от ботов)")
            print("2. Изменилась структура страницы")
            print("3. Нет интернет-соединения")
            print("\nПопробуйте:")
            print("- Запустить скрипт позже")
            print("- Использовать VPN")
            print("- Использовать локальный HTML файл (run_actor_parser.py)")
        
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
