'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { useUserInteractionsStore } from '@/store';

export const useHistoryTracker = () => {
  const pathname = usePathname();
  const { addFilmToHistory } = useUserInteractionsStore();

  useEffect(() => {
    const trackVisit = async () => {
      // Проверяем, что мы на странице фильма
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

    // Задержка для предотвращения дублирования при навигации
    const timeoutId = setTimeout(trackVisit, 500);

    return () => clearTimeout(timeoutId);
  }, [pathname, addFilmToHistory]);
};