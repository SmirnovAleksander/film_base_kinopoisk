# 🎬 Парсеры Кинопоиска

Комплексное решение для парсинга данных с сайта Кинопоиска с использованием BeautifulSoup4, lxml и requests.

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск парсеров

#### 📋 Парсинг списка фильмов
```bash
# Локальный HTML (рекомендуется)
python run_parser.py

# Онлайн парсинг
python run_online_parser.py
```

#### 🎬 Парсинг страницы отдельного фильма
```bash
# Локальный HTML
python run_film_parser.py

# Онлайн парсинг
python run_film_online_parser.py
```

#### 👤 Парсинг страницы актера
```bash
# Локальный HTML
python run_actor_parser.py

# Онлайн парсинг
python run_actor_online_parser.py
```

## 📁 Структура проекта

```
film_base_kinopoisk/
├── parser/
│   ├── kinopoisk_parser.py      # Парсер списка фильмов
│   ├── film_page_parser.py      # Парсер страницы фильма
│   ├── actor_page_parser.py     # Парсер страницы актера
│   └── cookies/
│       └── session.json         # Cookies для обхода защиты
├── templates/
│   ├── all_films_kinopoisk.html # HTML списка фильмов
│   ├── film_page_kinopoisk.html # HTML страницы фильма
│   └── actor_page_kinopoisk.html # HTML страницы актера
├── output/                      # Результаты парсинга
│   ├── parsed_films.json       # Список фильмов
│   ├── online_parsed_films.json # Онлайн список
│   ├── film_details.json       # Детали фильма
│   └── actor_details.json      # Детали актера
├── requirements.txt            # Зависимости
└── README.md                   # Документация
```

## 🛠️ Возможности парсеров

### 📋 Парсер списка фильмов
- **Название фильма** (русское и оригинальное)
- **Год выпуска**
- **Рейтинг** (Кинопоиск, IMDB)
- **Жанры**
- **Страны производства**
- **Режиссер**
- **Актеры**
- **Описание**
- **Постер**
- **Продолжительность**
- **Возрастной рейтинг**
- **ID фильма**

### 🎬 Парсер страницы фильма
- Все данные из списка фильмов
- **Детальное описание**
- **Бюджет фильма**
- **Кассовые сборы**
- **Дата премьеры**
- **Студия производства**
- **Оригинальное название**
- **Рейтинг IMDB**

### 👤 Парсер страницы актера
- **Имя и полное имя**
- **Дата и место рождения**
- **Национальность**
- **Профессии**
- **Рост**
- **Биография**
- **Фото**
- **Фильмография**
- **Награды**
- **Образование**
- **Семейная информация**

## 🔧 Методы парсинга

### 1. JSON данные
- Извлечение из script тегов
- Рекурсивный обход структур
- Обработка сложных объектов

### 2. HTML элементы
- Поиск по CSS селекторам
- Извлечение из meta тегов
- Обработка различных форматов

### 3. Обход защиты
- Ротация User-Agent
- Задержки между запросами
- Использование cookies
- Мобильные заголовки

## 📊 Примеры использования

### Базовое использование

```python
from parser.kinopoisk_parser import KinopoiskParser
from parser.film_page_parser import FilmPageParser

# Парсинг списка фильмов
parser = KinopoiskParser()
parser.load_html_from_file('templates/all_films_kinopoisk.html')
films = parser.parse_all_films()

# Парсинг страницы фильма
film_parser = FilmPageParser()
film_parser.load_html_from_file('templates/film_page_kinopoisk.html')
film_data = film_parser.extract_film_details()

# Парсинг страницы актера
actor_parser = ActorPageParser()
actor_parser.load_html_from_file('templates/actor_page_kinopoisk.html')
actor_data = actor_parser.extract_actor_details()
```

### Онлайн парсинг

```python
# Парсинг с сайта
parser = KinopoiskParser()
parser.load_html_from_url('https://www.kinopoisk.ru/lists/movies/?b=films')
films = parser.parse_all_films()

# Парсинг страницы фильма
film_parser = FilmPageParser()
film_parser.load_html_from_url('https://www.kinopoisk.ru/film/535341/')
film_data = film_parser.extract_film_details()

# Парсинг страницы актера
actor_parser = ActorPageParser()
actor_parser.load_html_from_url('https://www.kinopoisk.ru/name/41644/')
actor_data = actor_parser.extract_actor_details()
```

## 🚨 Важные замечания

### Защита от ботов
Сайт Кинопоиска использует **SmartCaptcha** для защиты от автоматических запросов. Рекомендации:

1. **Используйте локальные HTML файлы** для разработки
2. **Настройте cookies** для обхода защиты
3. **Используйте VPN** при необходимости
4. **Добавьте задержки** между запросами

### Правовые аспекты
- ✅ Используйте для личных целей
- ✅ Соблюдайте robots.txt
- ✅ Не перегружайте сервер
- ❌ Не используйте для коммерческих целей без разрешения

## 🔧 Настройка

### Cookies для обхода защиты

1. Откройте Кинопоиск в браузере
2. Войдите в аккаунт
3. Скопируйте cookies в `parser/cookies/session.json`

**Формат:**
```json
{
  "cookies": {
    "session_id": "your_session_value",
    "user_token": "your_token"
  }
}
```

## 📈 Примеры результатов

### Список фильмов
```json
[
  {
    "title": "1+1",
    "year": "2011",
    "rating": "8.857",
    "genres": ["драма", "комедия"],
    "countries": ["Франция"],
    "director": "Оливье Накаш",
    "duration": "112",
    "id": "535341"
  }
]
```

### Детали фильма
```json
{
  "title": "1+1",
  "original_title": "Intouchables",
  "year": "2011",
  "rating": "8.857",
  "imdb_rating": "8.5",
  "genres": ["драма", "комедия"],
  "countries": ["Франция"],
  "director": "Оливье Накаш",
  "actors": ["Франсуа Клюзе", "Омар Си"],
  "description": "Аристократ на коляске нанимает в сиделки бывшего заключенного...",
  "budget": "9,500,000 €",
  "box_office": "426,588,510 $",
  "duration": "112",
  "id": "535341"
}
```

### Детали актера
```json
{
  "name": "Омар Си",
  "full_name": "Omar Sy",
  "birth_date": "1978-01-20",
  "birth_place": "Трап, Ивелин, Франция",
  "nationality": "Француз",
  "profession": ["Актер", "Продюсер", "Сценарист"],
  "height": "190",
  "biography": "Французский актер, комик и продюсер...",
  "photo": "https://avatars.mds.yandex.net/get-kinopoisk-image/...",
  "filmography": [
    {
      "title": "1+1",
      "year": "2011",
      "role": "Дрисс",
      "rating": "8.857"
    }
  ],
  "awards": ["Сезар", "Оскар"],
  "id": "41644"
}
```

## 🚀 Запуск

### Локальный парсинг (рекомендуется)
```bash
# Список фильмов
python run_parser.py

# Страница фильма
python run_film_parser.py

# Страница актера
python run_actor_parser.py
```

### Онлайн парсинг
```bash
# Список фильмов
python run_online_parser.py

# Страница фильма
python run_film_online_parser.py

# Страница актера
python run_actor_online_parser.py
```

## 🔗 Полезные ссылки

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Кинопоиск](https://www.kinopoisk.ru/)

---

**Удачного парсинга! 🎬**