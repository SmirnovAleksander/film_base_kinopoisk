import 'server-only';

import { cache } from 'react';
import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import { getSession, isSessionValid } from './session';
import { User } from '@/lib/types';

/**
 * Верификация сессии пользователя
 * Кэшируется на время рендера компонента
 */
export const verifySession = cache(async () => {
  const session = await getSession();
  
  if (!await isSessionValid(session)) {
    redirect('/login');
  }

  return { 
    isAuth: true, 
    userId: session!.userId,
    email: session!.email 
  };
});

/**
 * Безопасная проверка сессии (без redirect)
 */
export const checkSession = cache(async () => {
  const session = await getSession();
  
  if (!await isSessionValid(session)) {
    return { isAuth: false, userId: null, email: null };
  }

  return { 
    isAuth: true, 
    userId: session!.userId,
    email: session!.email 
  };
});

/**
 * Получение данных пользователя через DAL
 */
export const getUser = cache(async () => {
  const session = await verifySession();
  if (!session) return null;

  try {
    // Импортируем AuthAPI динамически для избежания проблем с SSR
    const { AuthAPI } = await import('@/lib/api/auth.api');
    
    const user = await AuthAPI.getCurrentUser();

    // Возвращаем только необходимые поля
    return {
      id: user.id,
      email: user.email,
      is_active: user.is_active,
      created_at: user.created_at,
    };
  } catch (error) {
    console.log('Failed to fetch user');
    return null;
  }
});

/**
 * Проверка роли пользователя (для будущего использования)
 */
export const checkUserRole = cache(async (requiredRole: string) => {
  const session = await verifySession();
  
  try {
    const user = await getUser();
    
    // Здесь можно добавить логику проверки ролей
    // Например, проверка is_admin или user_role
    return user?.id !== null; // Упрощенная проверка
  } catch (error) {
    console.log('Failed to check user role:', error);
    return false;
  }
});

/**
 * Защищенный API запрос
 */
export const authorizedFetch = cache(async (url: string, options: RequestInit = {}) => {
  const session = await verifySession();
  
  const tokenCookie = (await cookies()).get('film-base-token');
  
  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${tokenCookie?.value}`,
    'Content-Type': 'application/json',
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    redirect('/login');
  }

  return response;
});