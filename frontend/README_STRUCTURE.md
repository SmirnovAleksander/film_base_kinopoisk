# Film Base Frontend - Структура проекта

## 📁 Файловая структура

```
frontend/
├── app/                     # Next.js 14 App Router
│   ├── (auth)/             # Группа маршрутов аутентификации
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── films/              # Фильмы
│   │   ├── page.tsx        # Список фильмов
│   │   └── [id]/
│   │       └── page.tsx    # Детали фильма
│   ├── profile/            # Профиль пользователя
│   │   └── page.tsx
│   ├── bookmarks/          # Закладки
│   │   └── page.tsx
│   ├── history/            # История просмотров
│   │   └── page.tsx
│   ├── layout.tsx          # Основной layout
│   ├── page.tsx            # Главная страница
│   └── globals.css         # Глобальные стили
├── components/             # React компоненты
│   ├── ui/                 # Базовые UI компоненты (shadcn/ui)
│   ├── layout/             # Layout компоненты
│   ├── film/               # Компоненты фильмов
│   ├── auth/               # Компоненты аутентификации
│   └── common/             # Общие компоненты
├── lib/                    # Утилиты и конфигурация
│   ├── api/                # API клиенты и запросы
│   ├── types/              # TypeScript типы
│   ├── utils/              # Вспомогательные функции
│   └── config.ts           # Конфигурация приложения
├── store/                  # Zustand stores
│   ├── auth.store.ts       # Аутентификация
│   ├── films.store.ts      # Фильмы
│   ├── user.store.ts       # Пользовательские данные
│   ├── ui.store.ts         # UI состояние (тема)
│   └── index.ts            # Экспорты store
├── hooks/                  # Custom React hooks
│   ├── use-auth.ts         # Хук аутентификации
│   ├── use-films.ts        # Хук фильмов
│   └── use-theme.ts        # Хук темы
└── public/                 # Статические файлы
```

## 🔧 Конфигурационные файлы

- `components.json` - конфигурация shadcn/ui
- `tailwind.config.ts` - настройки TailwindCSS
- `tsconfig.json` - настройки TypeScript
- `next.config.ts` - настройки Next.js
- `postcss.config.mjs` - настройки PostCSS

## 📡 API Endpoints (backend_new)

### Аутентификация
- `POST /auth/login` - вход
- `POST /auth/register` - регистрация  
- `POST /auth/logout` - выход
- `GET /users/me` - получить профиль

### Фильмы
- `GET /films/` - список фильмов
- `GET /films/search` - поиск фильмов
- `GET /films/{id}` - детали фильма
- `GET /films/filter` - фильтрация
- `GET /films/{id}/recommendations` - рекомендации

### Закладки
- `GET /bookmarks/` - список закладок
- `POST /bookmarks/{film_id}` - добавить
- `DELETE /bookmarks/{film_id}` - удалить

### Рейтинги
- `GET /ratings/films/{film_id}/rating` - получить рейтинг
- `POST /ratings/films/{film_id}/rating` - поставить рейтинг
- `DELETE /ratings/films/{film_id}/rating` - удалить рейтинг

### Комментарии
- `GET /comments/{film_id}` - список комментариев
- `POST /comments/{film_id}` - добавить комментарий
- `PUT /comments/{comment_id}` - редактировать
- `DELETE /comments/{comment_id}` - удалить