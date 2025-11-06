'use client';

import { ReactNode, useEffect } from 'react';
import { QueryProvider } from './query-provider';
import { AuthAPI } from '@/lib/api/auth.api';

interface AppProvidersProps {
  children: ReactNode;
}

function AuthInitializer() {
  useEffect(() => {
    // Инициализируем аутентификацию при загрузке приложения
    const token = AuthAPI.getAuthToken();
    const user = AuthAPI.getUserData();
    
    if (token && user) {
      console.log('🔑 AuthInitializer: Found existing auth data');
    } else {
      console.log('🔑 AuthInitializer: No existing auth data');
    }
  }, []);

  return null;
}

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryProvider>
      <AuthInitializer />
      {children}
    </QueryProvider>
  );
}