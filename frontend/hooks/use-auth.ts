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

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = AuthAPI.getAuthToken();
      const storedUser = AuthAPI.getUserData();
      
      if (storedToken && storedUser && !token && !user) {
        console.log('useAuth: Found stored auth data, syncing store');
        useAuthStore.setState({
          token: storedToken,
          user: storedUser,
          isAuthenticated: true,
        });
      } else if (storedToken && !user) {
        console.log('useAuth: Token found but no user, fetching user data');
        try {
          await getCurrentUser();
        } catch (error) {
          console.warn('useAuth: Failed to get current user:', error);
          clearAuth();
        }
      } else {
        console.log('useAuth: No stored auth data');
      }
      setIsInitialized(true);
    };

    initAuth();
  }, [token, user, getCurrentUser, clearAuth]);

  return {
    user,
    token,
    isLoading: isLoading || !isInitialized,
    isAuthenticated,
    isInitialized,
    
    login,
    register,
    logout,
    getCurrentUser,
    updateUser,
    clearAuth,
    setLoading,
    
    isLoggedIn: isAuthenticated,
    isAdmin: user?.is_superuser || false,
    isVerified: user?.is_verified || false,
  };
}