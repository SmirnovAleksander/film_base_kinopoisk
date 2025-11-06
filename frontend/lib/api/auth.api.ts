import { apiClient } from './client.api';
import {
  LoginData,
  RegisterData,
  User,
} from '@/lib/types';
import { API_ENDPOINTS, STORAGE_KEYS } from '@/lib/config';

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
    // Очищаем localStorage
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

  // Утилиты для работы с localStorage
  static setAuthData(accessToken: string, user: User): void {
    if (typeof window === 'undefined') {
      console.warn('🔑 AuthAPI: Cannot set auth data - not in browser environment');
      return;
    }
    
    if (!this.isLocalStorageAvailable()) {
      console.error('🔑 AuthAPI: localStorage not available');
      return;
    }
    
    try {
      // Сохраняем в localStorage
      localStorage.setItem(TOKEN_KEY, accessToken);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      authEvents.emit(); // Уведомляем об изменении токена
      console.log('🔑 AuthAPI: Auth data stored in localStorage');
      console.log('🔑 AuthAPI: Token length:', accessToken.length);
      console.log('🔑 AuthAPI: User:', user.username);
    } catch (error) {
      console.error('Failed to store auth data:', error);
    }
  }

  static getAuthToken(): string | null {
    if (typeof window === 'undefined') {
      console.log('🔑 AuthAPI: getAuthToken called on server side');
      return null;
    }
    
    if (!this.isLocalStorageAvailable()) {
      console.error('🔑 AuthAPI: localStorage not available');
      return null;
    }
    
    try {
      const token = localStorage.getItem(TOKEN_KEY);
      console.log('🔑 AuthAPI: Retrieved token:', token ? `${token.substring(0, 20)}...` : 'null');
      console.log('🔑 AuthAPI: localStorage keys:', Object.keys(localStorage));
      return token;
    } catch (error) {
      console.error('Failed to get auth token:', error);
      return null;
    }
  }

  static getUserData(): User | null {
    if (typeof window === 'undefined') {
      console.log('🔑 AuthAPI: getUserData called on server side');
      return null;
    }
    
    if (!this.isLocalStorageAvailable()) {
      console.error('🔑 AuthAPI: localStorage not available');
      return null;
    }
    
    try {
      const userData = localStorage.getItem(USER_KEY);
      const parsed = userData ? JSON.parse(userData) : null;
      console.log('🔑 AuthAPI: Retrieved user data:', parsed?.username || 'null');
      return parsed;
    } catch (error) {
      console.error('Failed to get user data:', error);
      return null;
    }
  }

  static clearAuthData(): void {
    if (typeof window === 'undefined') {
      console.warn('🔑 AuthAPI: Cannot clear auth data - not in browser environment');
      return;
    }
    
    if (!this.isLocalStorageAvailable()) {
      console.error('🔑 AuthAPI: localStorage not available');
      return;
    }
    
    try {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      authEvents.emit(); // Уведомляем об очистке токена
      console.log('🔑 AuthAPI: Auth data cleared from localStorage');
    } catch (error) {
      console.error('Failed to clear auth data:', error);
    }
  }

  // Проверка актуальности токена
  static isTokenValid(): boolean {
    return this.getAuthToken() !== null;
  }

  // Подписка на изменения токена
  static onAuthChange(callback: () => void): () => void {
    return authEvents.onChange(callback);
  }

  // Проверка доступности localStorage
  static isLocalStorageAvailable(): boolean {
    if (typeof window === 'undefined') return false;
    
    try {
      const test = '__localStorage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch (error) {
      console.error('localStorage not available:', error);
      return false;
    }
  }

  // Диагностика состояния localStorage
  static debugLocalStorage(): void {
    if (typeof window === 'undefined') {
      console.log('🔍 AuthAPI Debug: Running on server side');
      return;
    }
    
    console.log('🔍 AuthAPI Debug: localStorage available:', this.isLocalStorageAvailable());
    console.log('🔍 AuthAPI Debug: localStorage keys:', Object.keys(localStorage));
    console.log('🔍 AuthAPI Debug: TOKEN_KEY exists:', localStorage.getItem(TOKEN_KEY) !== null);
    console.log('🔍 AuthAPI Debug: USER_KEY exists:', localStorage.getItem(USER_KEY) !== null);
    console.log('🔍 AuthAPI Debug: Token value:', localStorage.getItem(TOKEN_KEY) ? `${localStorage.getItem(TOKEN_KEY)?.substring(0, 20)}...` : 'null');
    
    try {
      const userData = localStorage.getItem(USER_KEY);
      if (userData) {
        const parsed = JSON.parse(userData);
        console.log('🔍 AuthAPI Debug: User data:', parsed);
      } else {
        console.log('🔍 AuthAPI Debug: No user data');
      }
    } catch (error) {
      console.log('🔍 AuthAPI Debug: Error parsing user data:', error);
    }
  }
}