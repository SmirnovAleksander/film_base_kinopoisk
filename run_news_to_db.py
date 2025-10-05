#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга новостей и сохранения в БД
"""

import os
import sys
from datetime import datetime

# Добавляем путь к модулям парсера
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser.news_page_parser import NewsPageParser
from main_parser import MainParser


def main():
    """Основная функция для парсинга новостей и сохранения в БД"""
    print("🚀 Запуск парсера новостей с сохранением в БД")
    
    try:
        # Создаем парсер новостей
        news_parser = NewsPageParser()
        
        # Парсим новости с 5 страниц
        print("📄 Парсинг новостей с 5 страниц...")
        news_list = news_parser.parse_multiple_pages(5)
        
        if news_list:
            print(f"✅ Найдено {len(news_list)} новостей")
            
            # Создаем главный парсер для работы с БД
            main_parser = MainParser()
            
            # Сохраняем новости в БД
            print("💾 Сохранение новостей в БД...")
            main_parser.save_news_to_db(news_list)
            
            # Закрываем соединение с БД
            main_parser.close_connection()
            
            print("✅ Парсинг и сохранение завершены успешно!")
        else:
            print("❌ Новости не найдены")
            
    except Exception as e:
        print(f"❌ Ошибка при парсинге новостей: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
