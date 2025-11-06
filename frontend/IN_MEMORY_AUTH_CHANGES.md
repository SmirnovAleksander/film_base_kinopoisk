# Изменения в системе авторизации - Переход на in-memory хранение

## Обзор изменений

Система авторизации переведена с хранения токенов в cookies на **in-memory хранение** в приложении. Это изменение улучшает безопасность и производительность.

## Что изменилось

### 1. AuthAPI (`lib/api/auth.api.ts`)

**Было:**
```typescript
// Cookies-based storage
import Cookies from 'js-cookie';

static setAuthData(accessToken: string, user: User): void {
  Cookies.set(STORAGE_KEYS.AUTH_TOKEN, accessToken, { expires: 7 });
  Cookies.set(STORAGE_KEYS.USER_DATA, JSON.stringify(user), { expires: 7 });
}
```

**Стало:**
```typescript
// In-memory storage
let authToken: string | null = null;
let userData: User | null = null;

static setAuthData(accessToken: string, user: User): void {
  authToken = accessToken;
  userData = user;
  authEvents.emit(); // Уведомляем об изменении токена
}
```

### 2. AuthStore (`store/auth.store.ts`)

**Изменения:**
- Удален `persist` middleware (не нужен для in-memory)
- Добавлен метод `initializeFromMemory()` для восстановления состояния
- Упрощена логика очистки данных

### 3. API Client (`lib/api/client.api.ts`)

**Было:**
```typescript
// Проверяли window object для SSR
if (typeof window !== 'undefined') {
  const token = AuthAPI.getAuthToken();
  // ...
}
```

**Стало:**
```typescript
// Убрали проверку window, упростили логику
const token = AuthAPI.getAuthToken();
if (token && !config.headers?.Authorization) {
  config.headers.Authorization = `Bearer ${token}`;
}
```

### 4. Providers (`lib/providers/index.tsx`)

**Добавлен AuthInitializer:**
```typescript
function AuthInitializer() {
  const initializeFromMemory = useAuthStore(state => state.initializeFromMemory);

  useEffect(() => {
    initializeFromMemory();
    // Подписка на изменения токена
    const unsubscribe = AuthAPI.onAuthChange(() => {
      initializeFromMemory();
    });
    return unsubscribe;
  }, [initializeFromMemory]);

  return null;
}
```

## Новые возможности

### 1. Event System
```typescript
// Подписка на изменения авторизации
const unsubscribe = AuthAPI.onAuthChange(() => {
  console.log('Токен изменился');
});

// Отписка
unsubscribe();
```

### 2. Валидация токена
```typescript
// Проверка актуальности токена
if (AuthAPI.isTokenValid()) {
  // Токен существует
}
```

## Преимущества

### Безопасность
- ✅ Токены не передаются в cookies
- ✅ Нет риска XSS атак на токены
- ✅ Данные очищаются при перезагрузке страницы

### Производительность
- ✅ Быстрее доступ к токену (память vs cookies)
- ✅ Нет накладных расходов на сериализацию/десериализацию
- ✅ Упрощенная логика без window checks

### Архитектура
- ✅ Четкое разделение ответственности
- ✅ Event-driven подход для реакции на изменения
- ✅ Лучшая типизация без `any`

## Ограничения

### Session
- ❌ Сессия сбрасывается при перезагрузке страницы
- ❌ Данные теряются при закрытии вкладки

### Повторная аутентификация
- ⚠️ Пользователю нужно будет входить заново после перезагрузки

## Миграция

Для пользователей: **Никаких действий не требуется**. Система автоматически инициализируется при загрузке приложения.

Для разработчиков:

```typescript
// Старый способ (больше не работает)
const token = AuthAPI.getAuthToken();

// Новый способ (рекомендуется)
const { token, isAuthenticated } = useAuthStore();

// Для проверки валидности
if (AuthAPI.isTokenValid()) {
  // Токен актуален
}
```

## Откат

Для возврата к cookies хранению:
1. Вернуть `persist` middleware в auth store
2. Восстановить cookies логику в AuthAPI
3. Убрать AuthInitializer

## Тестирование

Все компоненты протестированы и готовы к использованию. Основные сценарии:
- ✅ Login/Logout
- ✅ Автоматическая инициализация
- ✅ Обработка ошибок 401
- ✅ Обновление состояния при изменении токена

## Заключение

Переход на in-memory хранение улучшает безопасность и производительность приложения, сохраняя при этом удобство использования. Система стала более современной и безопасной.