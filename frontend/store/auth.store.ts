import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthAPI } from '@/lib/api';
import {
  User,
  LoginData,
  RegisterData,
} from '@/lib/types';
import { STORAGE_KEYS } from '../lib/config';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  // Действия
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<User>;
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
      isLoading: false,
      isAuthenticated: false,

      login: async (data: LoginData) => {
        set({ isLoading: true });
        try {
          // OAuth2 вход - получаем только access_token
          const { access_token, token_type } = await AuthAPI.login(data);
          console.log('🔍 Login response:', { access_token: access_token.substring(0, 20) + '...', token_type });
          
          // КРИТИЧНО: Сначала сохраняем токен в cookies
          // Без этого getCurrentUser() не сможет аутентифицироваться
          AuthAPI.setAuthData(access_token, {} as User);
          
          // Теперь получаем данные пользователя с валидным токеном
          const user = await AuthAPI.getCurrentUser();
          console.log('🔍 User data:', user);

          // Обновляем cookies с реальными данными пользователя
          AuthAPI.setAuthData(access_token, user);
          
          // Проверяем, что данные сохранились
          const savedToken = AuthAPI.getAuthToken();
          const savedUser = AuthAPI.getUserData();
          console.log('🔍 Saved token:', savedToken ? savedToken.substring(0, 20) + '...' : 'null');
          console.log('🔍 Saved user:', savedUser);

          set({
            user,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          // Очищаем частичные данные в случае ошибки
          AuthAPI.clearAuthData();
          throw error;
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true });
        try {
          const user = await AuthAPI.register(data);
          
          // После регистрации нужно войти в систему
          set({ isLoading: false });
          return user;
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
          // Очищаем данные через AuthAPI
          AuthAPI.clearAuthData();

          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },

      getCurrentUser: async () => {
        const token = AuthAPI.getAuthToken();
        if (!token) {
          console.warn('getCurrentUser: No token available');
          get().clearAuth();
          throw new Error('No token available');
        }

        set({ isLoading: true });
        try {
          const user = await AuthAPI.getCurrentUser();
          
          // Обновляем данные в cookies
          AuthAPI.setAuthData(token, user);

          set({
            user,
            isAuthenticated: true,
            token,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          
          // Если ошибка авторизации (401), очищаем состояние
          if ((error as any)?.response?.status === 401) {
            console.warn('getCurrentUser: Token expired or invalid, clearing auth');
            get().clearAuth();
          } else {
            // Для других ошибок логируем, но не очищаем состояние
            console.error('getCurrentUser error:', error);
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
          
          // Обновляем данные в cookies
          const token = AuthAPI.getAuthToken();
          if (token) {
            AuthAPI.setAuthData(token, updatedUser);
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
        // Очищаем данные через AuthAPI
        AuthAPI.clearAuthData();

        set({
          user: null,
          token: null,
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
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);