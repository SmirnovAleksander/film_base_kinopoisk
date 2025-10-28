import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { API_CONFIG, STORAGE_KEYS } from '../config';
import { AuthAPI } from './auth';

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
    if (typeof window !== 'undefined') {
      // Используем AuthAPI для получения токена из cookies
      const token = AuthAPI.getAuthToken();
      if (token && !config.headers?.Authorization) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Интерцептор для обработки ответов и обновления токенов
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as RequestConfig;

    // Если ошибка 401 и не первая попытка
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Для OAuth2 нет refresh токена, поэтому просто очищаем состояние
        // НЕ перенаправляем автоматически на логин - пусть UI сам решает
        if (typeof window !== 'undefined') {
          AuthAPI.clearAuthData();
          // Убираем автоматическое перенаправление
          console.warn('Авторизация истекла. Требуется повторный вход.');
        }
      } catch (refreshError) {
        // Если произошла ошибка, очищаем cookies
        // НЕ перенаправляем автоматически
        if (typeof window !== 'undefined') {
          AuthAPI.clearAuthData();
          console.warn('Ошибка обновления авторизации. Требуется повторный вход.');
        }
      }
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