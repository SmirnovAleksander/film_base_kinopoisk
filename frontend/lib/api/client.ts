import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { API_CONFIG, STORAGE_KEYS } from '../config';

// Создаем экземпляр axios
export const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Типы для запросов
interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

interface RequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

// Интерцептор для добавления токена авторизации
apiClient.interceptors.request.use(
  (config: RequestConfig) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
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
        // Пытаемся обновить токен
        const refreshToken = localStorage.getItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
        if (refreshToken) {
          const response = await axios.post(`${API_CONFIG.baseURL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token } = response.data;
          localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
          
          // Обновляем токен в оригинальном запросе
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
          }
          
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Если не удалось обновить токен, очищаем localStorage и перенаправляем на логин
        if (typeof window !== 'undefined') {
          localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
          localStorage.removeItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
          localStorage.removeItem(STORAGE_KEYS.USER_DATA);
          window.location.href = '/(auth)/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

// Функция для проверки, авторизован ли пользователь
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false;
  const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  return !!token;
};

// Функция для выхода
export const logout = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    localStorage.removeItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
    localStorage.removeItem(STORAGE_KEYS.USER_DATA);
    window.location.href = '/(auth)/login';
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