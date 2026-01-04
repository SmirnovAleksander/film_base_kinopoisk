#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для извлечения данных о фильмах с Кинопоиска
Использует BeautifulSoup4 и lxml для парсинга HTML
"""

import json
import os
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base_parser import BaseParser


class KinopoiskParser(BaseParser):
    """Парсер для извлечения данных о фильмах с Кинопоиска"""
    
    def load_html_from_file(self, file_path: str = None) -> BeautifulSoup:
        """
        Загружает HTML из файла
        
        Args:
            file_path: Путь к HTML файлу
            
        Returns:
            BeautifulSoup объект
        """
        if file_path:
            self.html_file_path = file_path
            
        return super().load_html_from_file(file_path)
    
    def load_html_from_url(self, url: str) -> BeautifulSoup:
        """Загружает HTML с веб-страницы Кинопоиска"""
        return super().load_html_from_url(url)
    
    
    
    def parse_all_films(self) -> List[Dict]:
        """
        Парсит все доступные данные о фильмах
        
        Returns:
            Список всех найденных фильмов
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        films = []
        
        # Извлекаем ID фильмов из ссылок (data-tid="23a2a59")
        film_links = self.soup.find_all('a', {'data-tid': '23a2a59'})
        
        valid_links = 0
        invalid_links = 0
        
        for i, link in enumerate(film_links):
            href = link.get('href')
            
            if href and '/film/' in href:
                valid_links += 1
                # Извлекаем ID из URL /film/535341/ -> 535341
                href_parts = href.split('/film/')
                if len(href_parts) > 1:
                    film_id = href_parts[1].rstrip('/')
                    
                    # Ищем название фильма в атрибуте alt изображения
                    film_name = None
                    img = link.find('img')
                    if img and img.get('alt'):
                        film_name = img.get('alt').strip()
                    
                    film_data = {'id': film_id}
                    if film_name:
                        film_data['name'] = film_name
                    
                    films.append(film_data)
                else:
                    pass
            else:
                invalid_links += 1
        
        return films
    
    def save_to_json(self, films: List[Dict], output_file: str = 'output/films_data.json'):
        """Сохраняет данные о фильмах в JSON файл"""
        super().save_to_json(films, output_file)
    
    def print_films_summary(self, films: List[Dict]):
        """
        Выводит краткую сводку по найденным фильмам
        
        Args:
            films: Список фильмов
        """
        print(f"\nНайдено фильмов: {len(films)}")
        print("-" * 50)
        
        for i, film in enumerate(films[:10], 1):  # Показываем первые 10
            title = film.get('title', 'Неизвестно')
            year = film.get('year', 'Неизвестно')
            rating = film.get('rating', 'Неизвестно')
            genres = film.get('genres', [])
            
            print(f"{i}. {title} ({year})")
            print(f"   Рейтинг: {rating}")
            if genres:
                print(f"   Жанры: {', '.join(genres)}")
            print()


def main():
    """Основная функция для демонстрации работы парсера"""
    # Создаем экземпляр парсера
    parser = KinopoiskParser()
    
    try:
        # Загружаем HTML из файла
        print("Загружаем HTML файл...")
        parser.load_html_from_file('templates/all_films_kinopoisk.html')
        
        # Парсим все фильмы
        print("Парсим данные о фильмах...")
        films = parser.parse_all_films()
        
        # Выводим сводку
        parser.print_films_summary(films)
        
        # Сохраняем в JSON
        parser.save_to_json(films, 'parsed_films.json')
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
