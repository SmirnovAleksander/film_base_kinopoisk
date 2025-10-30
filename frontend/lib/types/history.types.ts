// Типы для истории просмотров

export interface UserFilmHistory {
  id: number;
  user_id: number;
  film_id: number;
  visited_at: string;
  film: Film;
}

export interface UserFilmHistoryResponse {
  history: UserFilmHistory[];
  total: number;
}

export interface UserFilmHistoryStats {
  total_visits: number;
  visits_7d: number;
  visits_30d: number;
  favorite_genre?: string | null;
  favorite_genre_count: number;
}

export interface MessageResponse {
  message: string;
}

// Импорт для зависимостей
import type { Film } from './film.types';