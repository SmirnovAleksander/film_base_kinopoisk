import { apiClient } from './client';
import {
  LoginData,
  RegisterData,
  AuthResponse,
  User,
} from '../types/api';
import { API_ENDPOINTS } from '../config';

export class AuthAPI {
  // Вход в систему
  static async login(data: LoginData): Promise<AuthResponse> {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, {
      username: data.email,
      password: data.password,
    });
    return response.data;
  }

  // Регистрация
  static async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.REGISTER, {
      email: data.email,
      password: data.password,
      password_confirm: data.confirm_password,
      first_name: data.first_name,
      last_name: data.last_name,
      username: data.username,
    });
    return response.data;
  }

  // Выход из системы
  static async logout(): Promise<void> {
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
}