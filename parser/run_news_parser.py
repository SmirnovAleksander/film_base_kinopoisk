#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Локальный парсер новостей Кинопоиска
Парсит новости из сохраненного HTML файла
"""

import os
import sys
import time
from datetime import datetime

# Добавляем путь к модулям парсера
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser_utils.news_page_parser import NewsPageParser


def main():
    """Основная функция локального парсера новостей"""
    print("🚀 Запуск локального парсера новостей")
    
    # Путь к HTML файлу
    html_file = "templates/news_page.html"
    
    # Проверяем существование файла
    if not os.path.exists(html_file):
        print(f"❌ HTML файл не найден: {html_file}")
        return 1
    
    try:
        # Создаем парсер
        parser = NewsPageParser()
        
        # Загружаем HTML из файла
        parser.load_html_from_file(html_file)
        
        if parser.soup:
            # Парсим новости
            news_list = parser.parse_news_list()
            
            # Собираем все данные
            result = {
                'news_list': news_list,
                'parsed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source_file': html_file,
                'total_news': len(news_list)
            }
            
            # Сохраняем результат
            filename = "output/news_local.json"
            parser.save_to_json(result, filename)
            
        else:
            print("❌ Не удалось загрузить HTML файл")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг прерван пользователем")
        return 1
    except Exception as e:
        print(f"\n❌ Ошибка при парсинге: {e}")
        return 1
    
    print("✅ Парсинг завершен")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
