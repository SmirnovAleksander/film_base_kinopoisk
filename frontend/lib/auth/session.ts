import 'server-only';

import { cookies } from 'next/headers';

// Определение типа сессии
export interface Session {
  userId: number;
  email: string;
  token: string;
}

// Константы из конфига
const STORAGE_KEYS = {
  AUTH_TOKEN: 'film-base-token',
  USER_DATA: 'film-base-user',
};

/**
 * Расшифровка сессии из cookies
 * Для простоты мы проверяем наличие токена и данных пользователя
 */
export async function decrypt(cookieValue: string | undefined): Promise<Session | null> {
  if (!cookieValue) return null;

  try {
    // Получаем токен из cookies
    const tokenCookie = (await cookies()).get(STORAGE_KEYS.AUTH_TOKEN);
    const userCookie = (await cookies()).get(STORAGE_KEYS.USER_DATA);

    if (!tokenCookie || !userCookie) return null;

    const userData = JSON.parse(userCookie.value);

    return {
      userId: userData.id,
      email: userData.email,
      token: tokenCookie.value,
    };
  } catch (error) {
    console.error('Failed to decrypt session:', error);
    return null;
  }
}

/**
 * Проверка валидности сессии
 */
export async function isSessionValid(session: Session | null): Promise<boolean> {
  return session !== null && session.userId > 0 && session.token.length > 0;
}

/**
 * Получение информации о пользователе из сессии
 */
export async function getSession(): Promise<Session | null> {
  try {
    const tokenCookie = (await cookies()).get(STORAGE_KEYS.AUTH_TOKEN);
    const userCookie = (await cookies()).get(STORAGE_KEYS.USER_DATA);

    if (!tokenCookie || !userCookie) return null;

    const userData = JSON.parse(userCookie.value);

    return {
      userId: userData.id,
      email: userData.email,
      token: tokenCookie.value,
    };
  } catch (error) {
    console.error('Failed to get session:', error);
    return null;
  }
}

/**
 * Создание сессии (для будущего использования)
 */
export async function createSession(userData: any, token: string): Promise<void> {
  // В реальном приложении здесь была бы логика создания сессии в БД
  console.log('Creating session for user:', userData.id);
}