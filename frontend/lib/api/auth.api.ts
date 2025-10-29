import { apiClient } from './client.api';
import Cookies from 'js-cookie';
import {
  LoginData,
  RegisterData,
  User,
} from '@/lib/types';
import { API_ENDPOINTS, STORAGE_KEYS } from '@/lib/config';

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
    });
    return response.data;
  }

  // Выход из системы
  static async logout(): Promise<void> {
    // Очищаем cookies
    Cookies.remove(STORAGE_KEYS.AUTH_TOKEN);
    Cookies.remove(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
    Cookies.remove(STORAGE_KEYS.USER_DATA);
    
    await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT);
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

  // Утилиты для работы с cookies
  static setAuthData(accessToken: string, user: User): void {
    // Сохраняем в cookies сроком на 7 дней
    Cookies.set(STORAGE_KEYS.AUTH_TOKEN, accessToken, { expires: 7 });
    Cookies.set(STORAGE_KEYS.USER_DATA, JSON.stringify(user), { expires: 7 });
  }

  static getAuthToken(): string | null {
    return Cookies.get(STORAGE_KEYS.AUTH_TOKEN) || null;
  }

  static getUserData(): User | null {
    const userData = Cookies.get(STORAGE_KEYS.USER_DATA);
    return userData ? JSON.parse(userData) : null;
  }

  static clearAuthData(): void {
    Cookies.remove(STORAGE_KEYS.AUTH_TOKEN);
    Cookies.remove(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
    Cookies.remove(STORAGE_KEYS.USER_DATA);
  }
}