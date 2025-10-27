#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Онлайн парсер новостей Кинопоиска
Парсит новости с сайта в реальном времени
"""

import os
import sys
import time
from datetime import datetime

# Добавляем путь к модулям парсера
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser_utils.news_page_parser import NewsPageParser


def main():
    """Основная функция онлайн парсера новостей"""
    print("🚀 Запуск онлайн парсера новостей")
    
    # URL для парсинга новостей
    news_url = "https://www.kinopoisk.ru/media/"
    
    try:
        # Создаем парсер
        parser = NewsPageParser()
        
        # Парсим новости с 5 страниц
        news_list = parser.parse_multiple_pages(5)
        
        if news_list:
            # Собираем все данные
            result = {
                'news_list': news_list,
                'parsed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source_url': news_url,
                'total_news': len(news_list)
            }
            
            # Сохраняем результат
            filename = "output/news_online.json"
            parser.save_to_json(result, filename)
            
        else:
            print("❌ Не удалось загрузить страницу")
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
