#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер для страницы актера на Кинопоиске
Извлекает детальную информацию об актере
"""

import json
from typing import Dict
from bs4 import BeautifulSoup
from .base_parser import BaseParser


class ActorPageParser(BaseParser):
    """Парсер для страницы актера"""
    
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
    
    def extract_actor_details(self) -> Dict:
        """
        Извлекает детальную информацию об актере из HTML элементов
        
        Returns:
            Словарь с детальной информацией об актере
        """
        if not self.soup:
            raise ValueError("HTML не загружен. Сначала вызовите load_html_from_file() или load_html_from_url()")
        
        actor_data = {}
        
        # Извлекаем данные из HTML элементов
        html_data = self._extract_from_html()
        if html_data:
            actor_data.update(html_data)
        
        # Извлекаем данные из meta тегов
        meta_data = self._extract_from_meta()
        if meta_data:
            actor_data.update(meta_data)
        
        return actor_data
    
    def _extract_from_html(self) -> Dict:
        """Извлекает данные из HTML элементов"""
        actor_data = {}
        
        # Извлекаем жанры (контейнер data-tid="e32f6be5", кнопки data-tid="9758b27c")
        genres_container = self.soup.find('div', {'data-tid': 'e32f6be5'})
        if genres_container:
            genre_buttons = genres_container.find_all('button', {'data-tid': '9758b27c'})
            genres = []
            for btn in genre_buttons:
                text = btn.get_text(strip=True)
                if text:
                    genres.append(text)
            if genres:
                actor_data['genres'] = genres
        
        # Извлекаем рост (data-test-id="height")
        height_elem = self.soup.find('div', {'data-test-id': 'height'})
        if height_elem:
            height_div = height_elem.find('div', {'data-tid': 'e1e37c21'})
            if height_div:
                height_text = height_div.get_text(strip=True)
                # Конвертируем метры в сантиметры
                if 'м' in height_text:
                    try:
                        # Извлекаем число из строки типа "1.9 м"
                        height_value = float(height_text.replace(' м', '').replace('м', ''))
                        # Конвертируем в сантиметры
                        height_cm = int(height_value * 100)
                        actor_data['height'] = str(height_cm)
                    except ValueError:
                        actor_data['height'] = height_text
                else:
                    actor_data['height'] = height_text
        
        # Извлекаем дату рождения (data-test-id="birthday")
        birthday_elem = self.soup.find('div', {'data-test-id': 'birthday'})
        if birthday_elem:
            birthday_div = birthday_elem.find('div', {'data-tid': '71455188'})
            if birthday_div:
                # # Извлекаем отдельные компоненты
                # day_month_link = birthday_div.find('a', href=lambda x: x and 'birthday' in x and 'day' in x and 'month' in x)
                # if day_month_link:
                #     actor_data['birthday_day_month'] = day_month_link.get_text(strip=True)
                
                # year_link = birthday_div.find('a', href=lambda x: x and 'birthday' in x and 'year' in x)
                # if year_link:
                #     actor_data['birthday_year'] = year_link.get_text(strip=True)
                
                zodiac_link = birthday_div.find('a', href=lambda x: x and 'zodiac' in x)
                if zodiac_link:
                    actor_data['zodiac'] = zodiac_link.get_text(strip=True)
                
                # # Извлекаем возраст
                # age_span = birthday_div.find('span', class_='styles_valueDark__jsGKY')
                # if age_span:
                #     age_text = age_span.get_text(strip=True)
                #     # Извлекаем только число из "47 лет"
                #     import re
                #     age_match = re.search(r'(\d+)', age_text)
                #     if age_match:
                #         actor_data['age'] = age_match.group(1)
        
        # Извлекаем место рождения (data-test-id="placeOfBirthday")
        birthplace_elem = self.soup.find('div', {'data-test-id': 'placeOfBirthday'})
        if birthplace_elem:
            birthplace_div = birthplace_elem.find('div', {'data-tid': '222c6c05'})
            if birthplace_div:
                # Извлекаем все ссылки с местами
                location_links = birthplace_div.find_all('a', {'data-tid': '46e19321'})
                locations = []
                for link in location_links:
                    location_text = link.get_text(strip=True)
                    if location_text:
                        locations.append(location_text)
                
                if locations:
                    actor_data['birthplace'] = locations
        
        # Извлекаем семейную информацию (data-test-id="partner")
        partner_elem = self.soup.find('div', {'data-test-id': 'partner'})
        if partner_elem:
            partner_ul = partner_elem.find('ul', {'data-tid': 'eb7e5e48'})
            if partner_ul:
                partner_lis = partner_ul.find_all('li', {'data-tid': '4f89888f'})
                spouse_names = []
                children_list = []
                for li in partner_lis:
                    # Имя(я) могут быть ссылкой <a> или <span>
                    name_link = li.find('a', {'data-test-id': 'next-link'})
                    name_text = ''
                    if name_link:
                        name_text = name_link.get_text(strip=True)
                    else:
                        name_span = li.find('span', class_='styles_valueDark__jsGKY')
                        if name_span:
                            name_text = name_span.get_text(strip=True)
                    if name_text:
                        spouse_names.append(name_text)
                    # Количество детей
                    children_span = li.find('span', class_='styles_childrenCount__L7a53')
                    if children_span:
                        children_list.append(children_span.get_text(strip=True))
                if spouse_names:
                    actor_data['spouse'] = spouse_names
                if children_list:
                    actor_data['children'] = children_list
        
        # Извлекаем статистику фильмографии (data-test-id="filmographyTotal")
        filmography_elem = self.soup.find('div', {'data-test-id': 'filmographyTotal'})
        if filmography_elem:
            filmography_div = filmography_elem.find('div', {'data-tid': '16f1da45'})
            if filmography_div:
                # Извлекаем общее количество фильмов
                total_span = filmography_div.find('span')
                if total_span:
                    total_text = total_span.get_text(strip=True)
                    if total_text.isdigit():
                        actor_data['total_films'] = int(total_text)
                
                # Извлекаем годы работы
                year_buttons = filmography_div.find_all('button', {'data-tid': '10653ce8'})
                if len(year_buttons) >= 2:
                    start_year = year_buttons[0].get_text(strip=True)
                    end_year = year_buttons[1].get_text(strip=True)
                    
                    # Сохраняем отдельные поля для БД
                    try:
                        actor_data['career_start_year'] = int(start_year)
                        actor_data['career_end_year'] = int(end_year)
                        # Продолжительность больше не сохраняем
                    except ValueError:
                        pass
        
        # Извлекаем фото актера (data-tid="d813cf42")
        photo_elem = self.soup.find('img', {'data-tid': 'd813cf42'})
        if photo_elem and photo_elem.get('src'):
            photo_url = photo_elem.get('src')
            if photo_url.startswith('//'):
                photo_url = 'https:' + photo_url
            elif not photo_url.startswith('http'):
                photo_url = 'https://' + photo_url
            actor_data['image'] = photo_url
        
        return actor_data
    
    def _extract_from_meta(self) -> Dict:
        """Извлекает данные из JSON-LD (script[type='application/ld+json']).
        Берём основные поля актёра: name, alternateName, gender, jobTitle, birthDate.
        """
        result: Dict = {}
        try:
            for script in self.soup.find_all('script', type='application/ld+json'):
                raw = script.string or script.get_text()
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                except Exception:
                    continue
                nodes = data if isinstance(data, list) else [data]
                for node in nodes:
                    if not isinstance(node, dict):
                        continue
                    node_type = node.get('@type') or node.get('type')
                    if node_type == 'Person' or (isinstance(node_type, list) and 'Person' in node_type):
                        # Имя
                        if node.get('name'):
                            result['name'] = str(node.get('name'))
                        # Оригинальное имя / альтернативное
                        if node.get('alternateName'):
                            result['original_name'] = str(node.get('alternateName'))
                        # Пол
                        if node.get('gender'):
                            gender_raw = node.get('gender')
                            try:
                                gender_str = str(gender_raw)
                                # Берём последний сегмент после '/'
                                if '/' in gender_str:
                                    gender_str = gender_str.rstrip('/').split('/')[-1]
                                result['gender'] = gender_str
                            except Exception:
                                result['gender'] = str(gender_raw)
                        # Роли/должности (может быть строкой с перечислением через запятую или списком)
                        job_title = node.get('jobTitle')
                        if job_title:
                            if isinstance(job_title, list):
                                result['career'] = [str(x) for x in job_title if x]
                            else:
                                result['career'] = [str(job_title)]
                      
                        if node.get('birthDate'):
                            result['birth_date'] = str(node.get('birthDate'))
                            # Также попробуем заполнить год, если ещё не заполнен
                        return result
        except Exception:
            pass
        return result
    
    def save_to_json(self, actor_data: Dict, output_file: str = 'output/actor_details.json'):
        """Сохраняет данные об актере в JSON файл"""
        super().save_to_json(actor_data, output_file)
    
    def print_actor_details(self, actor_data: Dict):
        """
        Выводит детальную информацию об актере
        
        Args:
            actor_data: Данные об актере
        """
        print("\n=== Детальная информация об актере ===")
        print("-" * 50)
        
        # Основная информация
        if actor_data.get('name'):
            print(f"🎭 Имя: {actor_data['name']}")
        
        if actor_data.get('full_name'):
            print(f"📝 Полное имя: {actor_data['full_name']}")
        
        if actor_data.get('birth_date'):
            print(f"🎂 Дата рождения: {actor_data['birth_date']}")
        
        if actor_data.get('birth_place'):
            print(f"🌍 Место рождения: {actor_data['birth_place']}")
        
        if actor_data.get('nationality'):
            print(f"🏳️ Национальность: {actor_data['nationality']}")
        
        if actor_data.get('height'):
            print(f"📏 Рост: {actor_data['height']}")
        
        # Профессии
        if actor_data.get('profession'):
            professions = actor_data['profession']
            if isinstance(professions, list):
                print(f"💼 Профессии: {', '.join(professions)}")
            else:
                print(f"💼 Профессия: {professions}")
        
        # Фильмография
        if actor_data.get('filmography'):
            films = actor_data['filmography']
            print(f"\n🎬 Фильмография ({len(films)} фильмов):")
            for i, film in enumerate(films[:10], 1):  # Показываем первые 10
                title = film.get('title', 'Неизвестно')
                year = film.get('year', '')
                role = film.get('role', '')
                year_str = f" ({year})" if year else ""
                role_str = f" - {role}" if role else ""
                print(f"  {i}. {title}{year_str}{role_str}")
            
            if len(films) > 10:
                print(f"    ... и еще {len(films) - 10} фильмов")
        
        # Награды
        if actor_data.get('awards'):
            awards = actor_data['awards']
            if isinstance(awards, list):
                print(f"\n🏆 Награды: {', '.join(awards[:5])}")
                if len(awards) > 5:
                    print(f"    ... и еще {len(awards) - 5} наград")
            else:
                print(f"🏆 Награды: {awards}")
        
        # Образование
        if actor_data.get('education'):
            print(f"🎓 Образование: {actor_data['education']}")
        
        # Биография
        if actor_data.get('biography'):
            bio = actor_data['biography']
            if len(bio) > 300:
                bio = bio[:300] + "..."
            print(f"\n📖 Биография: {bio}")
        
        print()


def main():
    """Основная функция для демонстрации работы парсера"""
    parser = ActorPageParser()
    
    try:
        # Загружаем HTML из файла
        print("Загружаем HTML файл...")
        parser.load_html_from_file('templates/actor_page_kinopoisk.html')
        
        # Извлекаем детальную информацию
        print("Извлекаем детальную информацию об актере...")
        actor_data = parser.extract_actor_details()
        
        # Выводим результаты
        parser.print_actor_details(actor_data)
        
        # Сохраняем в JSON
        parser.save_to_json(actor_data, 'output/actor_details.json')
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
