'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
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
            retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
          },
          mutations: {
            retry: false,
            onError: (error: any) => {
              console.error('Mutation error:', error);
            },
            onSuccess: () => {
              console.log('Mutation successful');
            },
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}