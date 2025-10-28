import { useEffect } from 'react';
import { useAuthStore } from '@/store';

export function useAuth() {
  const {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    getCurrentUser,
    updateUser,
    clearAuth,
    setLoading,
  } = useAuthStore();

  // Проверяем авторизацию при загрузке приложения
  useEffect(() => {
    const initAuth = async () => {
      if (token && !user) {
        try {
          await getCurrentUser();
        } catch (error) {
          console.warn('Failed to get current user:', error);
          clearAuth();
        }
      }
    };

    initAuth();
  }, [token, user, getCurrentUser, clearAuth]);

  return {
    // Состояние
    user,
    token,
    isLoading,
    isAuthenticated,
    
    // Действия
    login,
    register,
    logout,
    getCurrentUser,
    updateUser,
    clearAuth,
    setLoading,
    
    // Утилиты
    isLoggedIn: isAuthenticated,
    isAdmin: user?.is_superuser || false,
    isVerified: user?.is_verified || false,
  };
}