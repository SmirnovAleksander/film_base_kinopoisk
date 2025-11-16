'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { useUserInteractionsStore } from '@/store';
import { useAuthStore } from '@/store';
import { isAuthenticated } from '@/lib/api';

export const useHistoryTracker = () => {
  const pathname = usePathname();
  const { addFilmToHistory } = useUserInteractionsStore();
  const { isAuthenticated: isUserAuthenticated } = useAuthStore();

  useEffect(() => {
    const trackVisit = async () => {
      if (!isUserAuthenticated && !isAuthenticated()) {
        return;
      }
      const filmMatch = pathname.match(/\/films\/(\d+)/);

      if (filmMatch) {
        const filmId = parseInt(filmMatch[1]);
        if (!isNaN(filmId)) {
          try {
            await addFilmToHistory(filmId);
          } catch (error) {
            console.error('Ошибка при добавлении фильма в историю:', error);
          }
        }
      }
    };

    const timeoutId = setTimeout(trackVisit, 500);

    return () => clearTimeout(timeoutId);
  }, [pathname, addFilmToHistory, isUserAuthenticated]);
};