import { useEffect, useState } from 'react';
import { useAuthStore } from '@/store';
import { AuthAPI } from '@/lib/api/auth.api';

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

  const [isInitialized, setIsInitialized] = useState(false);

  // Проверяем авторизацию при загрузке приложения
  useEffect(() => {
    const initAuth = async () => {
      // Проверяем наличие токена в localStorage
      const storedToken = AuthAPI.getAuthToken();
      const storedUser = AuthAPI.getUserData();
      
      console.log('🔑 useAuth: Init auth check');
      console.log('🔑 useAuth: Stored token:', storedToken ? `${storedToken.substring(0, 20)}...` : 'null');
      console.log('🔑 useAuth: Stored user:', storedUser?.username || 'null');
      
      if (storedToken && storedUser && !token && !user) {
        console.log('🔑 useAuth: Found stored auth data, syncing store');
        // Синхронизируем store с localStorage
        useAuthStore.setState({
          token: storedToken,
          user: storedUser,
          isAuthenticated: true,
        });
      } else if (storedToken && !user) {
        console.log('🔑 useAuth: Token found but no user, fetching user data');
        try {
          await getCurrentUser();
        } catch (error) {
          console.warn('🔑 useAuth: Failed to get current user:', error);
          clearAuth();
        }
      } else {
        console.log('🔑 useAuth: No stored auth data');
      }
      
      setIsInitialized(true);
    };

    initAuth();
  }, [token, user, getCurrentUser, clearAuth]);

  return {
    // Состояние
    user,
    token,
    isLoading: isLoading || !isInitialized,
    isAuthenticated,
    isInitialized,
    
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