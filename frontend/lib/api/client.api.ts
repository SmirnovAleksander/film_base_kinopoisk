import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { API_CONFIG } from '@/lib/config';
import { AuthAPI } from './auth.api';

// Создаем экземпляр axios
export const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Типы для запросов
interface RequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

// Интерцептор для добавления токена авторизации
apiClient.interceptors.request.use(
  (config: RequestConfig) => {
    // Всегда получаем свежий токен из localStorage
    const token = AuthAPI.getAuthToken();
    console.log('🔑 Request interceptor - Token:', token ? `${token.substring(0, 20)}...` : 'null');
    console.log('🔑 Request interceptor - URL:', config.url);
    console.log('🔑 Request interceptor - Method:', config.method?.toUpperCase());
    
    if (token) {
      // Удаляем существующий Authorization header и добавляем новый
      delete config.headers.Authorization;
      config.headers.Authorization = `Bearer ${token}`;
      console.log('✅ Added/Updated Authorization header:', `Bearer ${token.substring(0, 20)}...`);
    } else {
      console.warn('⚠️ No token available for authenticated request:', config.url);
    }
    
    // Дополнительная диагностика для отладки
    if (config.url?.includes('/bookmarks') ||
        config.url?.includes('/ratings') ||
        config.url?.includes('/users/me')) {
      console.log('🔍 Authenticated request detected - Token available:', !!token);
    }
    
    return config;
  },
  (error) => {
    console.error('❌ Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Интерцептор для обработки ответов и обновления токенов
apiClient.interceptors.response.use(
(response: AxiosResponse) => {
  console.log('✅ Response interceptor - Success:', response.config.url);
  return response;
},
async (error: AxiosError) => {
  const originalRequest = error.config as RequestConfig;
  const status = error.response?.status;
  const url = originalRequest?.url;
  
  console.log('❌ Response interceptor - Error:', status, url);
   
  // Диагностика состояния авторизации при ошибке 401
  if (status === 401) {
    const token = AuthAPI.getAuthToken();
    console.log('🔍 401 Error Diagnostics:');
    console.log('🔍 - Token available:', !!token);
    console.log('🔍 - Token value:', token ? `${token.substring(0, 20)}...` : 'null');
    console.log('🔍 - Request URL:', url);
    console.log('🔍 - Request method:', originalRequest?.method);
    console.log('🔍 - Request headers Authorization:', originalRequest?.headers?.Authorization ? 'present' : 'missing');
  }

  // Если ошибка 401 и не первая попытка
  if (status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    
    // Определяем, является ли запрос аутентифицированным
    const isAuthenticatedRequest = url?.includes('/bookmarks') ||
                                  url?.includes('/ratings') ||
                                  url?.includes('/users/') ||
                                  url?.includes('/comments') ||
                                  originalRequest?.headers?.Authorization;

    if (isAuthenticatedRequest) {
      console.warn('🔑 Authenticated request failed with 401 - Clearing auth data');
      
      try {
        // Очищаем localStorage
        AuthAPI.clearAuthData();
        console.warn('🔑 Авторизация истекла. Требуется повторный вход.');
        
        // Отправляем кастомное событие для уведомления UI
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('auth:expired', {
            detail: { message: 'Сессия истекла. Пожалуйста, войдите снова.' }
          }));
        }
      } catch (refreshError) {
        // Если произошла ошибка при очистке
        AuthAPI.clearAuthData();
        console.error('❌ Ошибка при очистке авторизации:', refreshError);
      }
    } else {
      console.log('🔍 Non-authenticated request failed with 401 - Ignoring');
    }
  } else if (status === 401) {
    // Вторая попытка с тем же токеном
    console.warn('🔑 Повторная ошибка 401 для:', url);
  }

  return Promise.reject(error);
}
);

// Функция для проверки, авторизован ли пользователь
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false;
  const token = AuthAPI.getAuthToken();
  return !!token;
};

// Функция для выхода
export const logout = (): void => {
  if (typeof window !== 'undefined') {
    AuthAPI.clearAuthData();
    window.location.href = '/login';
  }
};

// Утилита для обработки ошибок API
export const handleApiError = (error: AxiosError): string => {
  if (error.response?.status === 401) {
    return 'Неавторизован. Пожалуйста, войдите в систему.';
  } else if (error.response?.status === 403) {
    return 'Доступ запрещен.';
  } else if (error.response?.status === 404) {
    return 'Запрашиваемый ресурс не найден.';
  } else if (error.response?.status && error.response.status >= 500) {
    return 'Ошибка сервера. Попробуйте позже.';
  } else if (error.code === 'ECONNABORTED') {
    return 'Время ожидания запроса истекло.';
  } else if (error.code === 'NETWORK_ERROR') {
    return 'Ошибка сети. Проверьте подключение к интернету.';
  } else if (error.response?.data) {
    // Пытаемся извлечь сообщение об ошибке из ответа сервера
    const errorMessage = (error.response.data as any)?.detail || (error.response.data as any)?.message;
    if (errorMessage) {
      return Array.isArray(errorMessage) ? errorMessage.join(', ') : errorMessage;
    }
  }
  
  return 'Произошла неизвестная ошибка.';
};

// Утилита для создания URL с параметрами запроса
export const buildQueryString = (params: Record<string, any>): string => {
  const searchParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(item => searchParams.append(key, String(item)));
      } else {
        searchParams.append(key, String(value));
      }
    }
  });
  
  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : '';
};