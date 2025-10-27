#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация для парсера Кинопоиска
"""

# Настройки базы данных
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'film_base_kinopoisk',
    'user': 'postgres',
    'password': 'admin123'
}

# Настройки задержек (в секундах)
DELAYS = {
    'BETWEEN_FILMS': 2,      # Пауза между фильмами
    'BETWEEN_PEOPLE': 1,     # Пауза между участниками
    'BETWEEN_PAGES': 5,      # Пауза между страницами
    'BEFORE_REQUEST': 2      # Пауза перед HTTP запросом
}

# Настройки парсинга
PARSING_CONFIG = {
    'MAX_PAGES': 3,          # Максимальное количество страниц для парсинга
    'START_PAGE': 1,          # Начальная страница
    'MAX_RETRIES': 3,         # Максимальное количество попыток при ошибках
    'TIMEOUT': 30             # Таймаут для HTTP запросов
}

# Настройки логирования
LOGGING_CONFIG = {
    'SHOW_PROGRESS': True,    # Показывать прогресс парсинга
    'SHOW_DELAYS': True,      # Показывать информацию о паузах
    'VERBOSE': True          # Подробные логи
}

# Настройки почты
MAIL_CONFIG = {
    "MAIL_USERNAME": "aleksander50.500@gmail.com",  # Твоя почта Gmail
    "MAIL_PASSWORD": "yujb torm lmeg ywlw",     # Пароль приложения Gmail
    "MAIL_FROM": "aleksander50.500@gmail.com",      # От кого отправлять
    "MAIL_PORT": 587,                         # Порт SMTP
    "MAIL_SERVER": "smtp.gmail.com",          # SMTP сервер Gmail
    "MAIL_STARTTLS": True,                    # Использовать STARTTLS
    "MAIL_SSL_TLS": False,                    # Не использовать SSL
    "USE_CREDENTIALS": True,                 # Использовать аутентификацию
    "VALIDATE_CERTS": True,                   # Проверять сертификаты
    "FRONTEND_URL": "http://localhost:3000"   # URL фронтенда для ссылок
}
