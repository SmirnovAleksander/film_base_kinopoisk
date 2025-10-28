import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthAPI } from '../lib/api/auth';
import {
  User,
  LoginData,
  RegisterData,
} from '../lib/types/api';
import { STORAGE_KEYS } from '../lib/config';

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  // Действия
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  getCurrentUser: () => Promise<void>;
  updateUser: (userData: Partial<User>) => Promise<void>;
  clearAuth: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isLoading: false,
      isAuthenticated: false,

      login: async (data: LoginData) => {
        set({ isLoading: true });
        try {
          const response = await AuthAPI.login(data);
          const { access_token, refresh_token, user } = response;

          // Сохраняем токены в localStorage
          if (typeof window !== 'undefined') {
            localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
            localStorage.setItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`, refresh_token);
            localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
          }

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true });
        try {
          const response = await AuthAPI.register(data);
          const { access_token, refresh_token, user } = response;

          // Сохраняем токены в localStorage
          if (typeof window !== 'undefined') {
            localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
            localStorage.setItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`, refresh_token);
            localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
          }

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: async () => {
        set({ isLoading: true });
        try {
          await AuthAPI.logout();
        } catch (error) {
          // Игнорируем ошибку выхода, все равно очищаем локальное состояние
          console.warn('Logout API error:', error);
        } finally {
          // Очищаем localStorage
          if (typeof window !== 'undefined') {
            localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
            localStorage.removeItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
            localStorage.removeItem(STORAGE_KEYS.USER_DATA);
          }

          set({
            user: null,
            token: null,
            refreshToken: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },

      getCurrentUser: async () => {
        const { token } = get();
        if (!token) {
          throw new Error('No token available');
        }

        set({ isLoading: true });
        try {
          const user = await AuthAPI.getCurrentUser();
          
          // Обновляем данные пользователя в localStorage
          if (typeof window !== 'undefined') {
            localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
          }

          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          // Если ошибка авторизации, очищаем состояние
          if ((error as any)?.response?.status === 401) {
            get().clearAuth();
          }
          throw error;
        }
      },

      updateUser: async (userData: Partial<User>) => {
        const { user } = get();
        if (!user) {
          throw new Error('No user logged in');
        }

        set({ isLoading: true });
        try {
          const updatedUser = await AuthAPI.updateProfile(userData);
          
          // Обновляем данные пользователя в localStorage
          if (typeof window !== 'undefined') {
            localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(updatedUser));
          }

          set({
            user: updatedUser,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      clearAuth: () => {
        // Очищаем localStorage
        if (typeof window !== 'undefined') {
          localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
          localStorage.removeItem(`${STORAGE_KEYS.AUTH_TOKEN}_refresh`);
          localStorage.removeItem(STORAGE_KEYS.USER_DATA);
        }

        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
          isLoading: false,
        });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },
    }),
    {
      name: STORAGE_KEYS.AUTH_TOKEN,
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);