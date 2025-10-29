'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { AuthAPI } from '@/lib/api';
import { useAuthStore } from '@/store';
import { LoginData, RegisterData, User } from '@/lib/types';
import Cookies from 'js-cookie';
import { STORAGE_KEYS } from '@/lib/config';

// Query Keys
export const AUTH_QUERY_KEYS = {
  currentUser: ['auth', 'current-user'],
  user: (id: number) => ['auth', 'user', id],
} as const;

// Хук для получения текущего пользователя
export function useCurrentUser() {
  return useQuery({
    queryKey: AUTH_QUERY_KEYS.currentUser,
    queryFn: () => AuthAPI.getCurrentUser(),
    enabled: !!AuthAPI.getAuthToken(),
    staleTime: 5 * 60 * 1000, // 5 минут
    gcTime: 10 * 60 * 1000, // 10 минут
    retry: (failureCount, error: any) => {
      // Не повторяем запросы при 401, 403, 404
      if (error?.response?.status === 401 || 
          error?.response?.status === 403 || 
          error?.response?.status === 404) {
        return false;
      }
      return failureCount < 3;
    },
  });
}

// Хук для получения пользователя по ID
export function useUser(id: number) {
  return useQuery({
    queryKey: AUTH_QUERY_KEYS.user(id),
    queryFn: () => AuthAPI.getUserById(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
}

// Хук для входа в систему
export function useLogin() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: LoginData) => AuthAPI.login(data),
    onSuccess: async (response) => {
      // Сохраняем токен
      AuthAPI.setAuthData(response.access_token, { id: 0, email: '', is_active: true, is_verified: false, is_superuser: false });
      
      // Получаем данные пользователя
      const user = await AuthAPI.getCurrentUser();
      
      // Обновляем cookies с реальными данными пользователя
      AuthAPI.setAuthData(response.access_token, user);
      
      // Инвалидируем query пользователя
      queryClient.invalidateQueries({ queryKey: AUTH_QUERY_KEYS.currentUser });
    },
    onError: (error) => {
      console.error('Login error:', error);
    },
  });
}

// Хук для регистрации
export function useRegister() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: RegisterData) => AuthAPI.register(data),
    onSuccess: (user) => {
      console.log('Registration successful:', user);
    },
    onError: (error) => {
      console.error('Registration error:', error);
    },
  });
}

// Хук для выхода из системы
export function useLogout() {
  const queryClient = useQueryClient();
  const { clearAuth } = useAuthStore();

  return useMutation({
    mutationFn: () => AuthAPI.logout(),
    onSuccess: () => {
      // Очищаем Zustand состояние
      clearAuth();
      
      // Очищаем React Query кэш
      queryClient.removeQueries({ queryKey: AUTH_QUERY_KEYS.currentUser });
      queryClient.clear();
      
      // Очищаем cookies
      Cookies.remove(STORAGE_KEYS.AUTH_TOKEN);
      Cookies.remove(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
      Cookies.remove(STORAGE_KEYS.USER_DATA);
    },
    onError: (error) => {
      console.error('Logout error:', error);
    },
  });
}

// Хук для обновления профиля
export function useUpdateProfile() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (userData: Partial<User>) => AuthAPI.updateProfile(userData),
    onSuccess: (updatedUser) => {
      // Обновляем кэш текущего пользователя
      queryClient.setQueryData(AUTH_QUERY_KEYS.currentUser, updatedUser);
      
      // Инвалидируем связанные queries
      queryClient.invalidateQueries({ queryKey: AUTH_QUERY_KEYS.currentUser });
    },
    onError: (error) => {
      console.error('Update profile error:', error);
    },
  });
}

// Хук для подтверждения email
export function useVerifyEmail() {
  return useMutation({
    mutationFn: (token: string) => AuthAPI.verifyEmail(token),
    onSuccess: () => {
      console.log('Email verified successfully');
    },
    onError: (error) => {
      console.error('Email verification error:', error);
    },
  });
}

// Хук для запроса сброса пароля
export function useRequestPasswordReset() {
  return useMutation({
    mutationFn: (email: string) => AuthAPI.requestPasswordReset(email),
    onSuccess: () => {
      console.log('Password reset request sent');
    },
    onError: (error) => {
      console.error('Password reset request error:', error);
    },
  });
}

// Хук для сброса пароля
export function useResetPassword() {
  return useMutation({
    mutationFn: ({ token, newPassword }: { token: string; newPassword: string }) => 
      AuthAPI.resetPassword(token, newPassword),
    onSuccess: () => {
      console.log('Password reset successful');
    },
    onError: (error) => {
      console.error('Password reset error:', error);
    },
  });
}

// Хук для запроса токена верификации email
export function useRequestVerificationEmail() {
  return useMutation({
    mutationFn: () => AuthAPI.requestVerificationEmail(),
    onSuccess: () => {
      console.log('Verification email requested');
    },
    onError: (error) => {
      console.error('Verification email request error:', error);
    },
  });
}