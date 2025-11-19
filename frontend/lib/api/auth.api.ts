import { apiClient } from './client.api';
import {
  LoginData,
  RegisterData,
  User,
} from '@/lib/types';
import { API_ENDPOINTS, STORAGE_KEYS } from '@/lib/config';
import Cookies from 'js-cookie';

// Cookie options
const COOKIE_OPTIONS = {
  expires: 7, // 7 days
  path: '/',
  sameSite: 'Strict' as const,
  secure: process.env.NODE_ENV === 'production',
};

// LocalStorage ключи
const TOKEN_KEY = STORAGE_KEYS.AUTH_TOKEN;
const USER_KEY = STORAGE_KEYS.USER_DATA;

// Event emitter для уведомления об изменении токена
class AuthEventEmitter {
  private listeners: Set<() => void> = new Set();

  onChange(listener: () => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  emit() {
    this.listeners.forEach(listener => listener());
  }
}

export const authEvents = new AuthEventEmitter();

export class AuthAPI {
  // Вход в систему (OAuth2 формат)
  static async login(data: LoginData): Promise<{ access_token: string; token_type: string }> {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN,
      new URLSearchParams({
        grant_type: 'password',
        username: data.email,
        password: data.password,
        scope: '',
        client_id: '',
        client_secret: '',
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    return response.data;
  }

  // Регистрация
  static async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.REGISTER, {
      email: data.email,
      password: data.password,
      username: data.username,
      first_name: data.first_name,
      last_name: data.last_name,
    });
    return response.data;
  }

  // Выход из системы
  static async logout(): Promise<void> {
    // Очищаем данные
    this.clearAuthData();

    // Отправляем запрос на сервер для завершения сессии
    try {
      await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT);
    } catch (error) {
      // Игнорируем ошибку logout от сервера, локальные данные все равно очищены
      console.warn('Server logout error:', error);
    }
  }

  // Запросить токен верификации email
  static async requestVerificationEmail(): Promise<void> {
    await apiClient.post(API_ENDPOINTS.AUTH.REQUEST_VERIFY);
  }

  // Подтвердить email
  static async verifyEmail(token: string): Promise<void> {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.VERIFY, {
      token,
    });
    return response.data;
  }

  // Запросить сброс пароля
  static async requestPasswordReset(email: string): Promise<void> {
    await apiClient.post(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, {
      email,
    });
  }

  // Сбросить пароль
  static async resetPassword(token: string, newPassword: string): Promise<void> {
    await apiClient.post(API_ENDPOINTS.AUTH.RESET_PASSWORD, {
      token,
      new_password: newPassword,
    });
  }

  // Получить профиль пользователя
  static async getCurrentUser(): Promise<User> {
    const response = await apiClient.get(API_ENDPOINTS.USERS.ME);
    return response.data;
  }

  // Обновить профиль пользователя
  static async updateProfile(data: Partial<User>): Promise<User> {
    const response = await apiClient.patch(API_ENDPOINTS.USERS.UPDATE, data);
    return response.data;
  }

  // Получить пользователя по ID
  static async getUserById(id: number): Promise<User> {
    const response = await apiClient.get(API_ENDPOINTS.USERS.GET_BY_ID(id));
    return response.data;
  }

  // Обновить пользователя по ID (только для админа)
  static async updateUserById(id: number, data: Partial<User>): Promise<User> {
    const response = await apiClient.patch(API_ENDPOINTS.USERS.UPDATE_BY_ID(id), data);
    return response.data;
  }

  // Утилиты для работы с Auth Data
  static setAuthData(accessToken: string, user: User): void {
    // Сохраняем токен в Cookie
    Cookies.set(TOKEN_KEY, accessToken, COOKIE_OPTIONS);

    // Сохраняем пользователя в localStorage (для быстрого доступа на клиенте)
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(USER_KEY, JSON.stringify(user));
      } catch (error) {
        console.error('Failed to store user data in localStorage:', error);
      }
    }

    authEvents.emit(); // Уведомляем об изменении
    console.log('🔑 AuthAPI: Auth data stored (Token in Cookie, User in LocalStorage)');
  }

  static getAuthToken(): string | null {
    if (typeof window === 'undefined') {
      return null;
    }
    // Получаем токен из Cookie
    const token = Cookies.get(TOKEN_KEY);
    return token || null;
  }

  static getUserData(): User | null {
    if (typeof window === 'undefined') {
      return null;
    }

    try {
      const userData = localStorage.getItem(USER_KEY);
      const parsed = userData ? JSON.parse(userData) : null;
      return parsed;
    } catch (error) {
      console.error('Failed to get user data:', error);
      return null;
    }
  }

  static clearAuthData(): void {
    // Удаляем токен из Cookie
    Cookies.remove(TOKEN_KEY, { path: '/' });

    // Удаляем данные из localStorage
    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(USER_KEY);
      } catch (error) {
        console.error('Failed to clear user data from localStorage:', error);
      }
    }

    authEvents.emit(); // Уведомляем об очистке
    console.log('🔑 AuthAPI: Auth data cleared');
  }

  // Проверка актуальности токена
  static isTokenValid(): boolean {
    return !!this.getAuthToken();
  }

  // Подписка на изменения токена
  static onAuthChange(callback: () => void): () => void {
    return authEvents.onChange(callback);
  }

  // Диагностика
  static debugAuth(): void {
    const token = Cookies.get(TOKEN_KEY);
    console.log('🔍 AuthAPI Debug: Token in Cookie:', !!token);
    if (typeof window !== 'undefined') {
      console.log('🔍 AuthAPI Debug: User in LocalStorage:', !!localStorage.getItem(USER_KEY));
    }
  }
}