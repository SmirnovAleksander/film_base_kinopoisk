#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск онлайн-парсера галереи кадров по URL
По аналогии с остальными run_* скриптами
"""

import os
import json
from parser_utils.stills_page_parser import StillsPageParser


def main():
    urls = [
        'https://www.kinopoisk.ru/film/535341/stills/',
        'https://www.kinopoisk.ru/film/535341/wall/',
    ]
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


if __name__ == '__main__':
    main()


