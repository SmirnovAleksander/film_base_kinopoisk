#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск главного парсера фильмов и актеров
"""

from main_parser import MainParser

def main():
    """Главная функция запуска парсера"""
    print("🚀 Запуск главного парсера Кинопоиска")
    print("=" * 50)
    
    try:
        # Создаем экземпляр парсера
        parser = MainParser()
        
        # Запускаем парсинг
        parser.parse_all_films(start_page=1, max_pages=2)  # Начинаем с 2 страниц для теста
        
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 Парсинг завершен")

if __name__ == "__main__":
    main()
