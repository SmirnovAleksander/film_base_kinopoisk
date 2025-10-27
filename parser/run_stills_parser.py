#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск локального парсера галереи кадров из HTML-файла
По аналогии с остальными run_* скриптами
"""

import os
import json
from parser_utils.stills_page_parser import StillsPageParser


def main():
    html_file = 'templates/posters_page.html'
    parser = StillsPageParser()
    parser.load_html_from_file(html_file)
    # Структурированная информация
    items = parser.extract_stills_info()
    os.makedirs('output', exist_ok=True)
    out_all = 'output/stills_local.json'
    with open(out_all, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"✅ Найдено карточек: {len(items)}. Файл: {out_all}")


if __name__ == '__main__':
    main()


