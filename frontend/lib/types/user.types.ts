import type { Film } from './film.types';

// Типы для пользователей и их взаимодействий с фильмами

// Запись в истории просмотров пользователя
export interface UserFilmHistoryRecord {
  visited_at: string;
  film: Film;
}

// Ответ для истории просмотров пользователя
export interface UserFilmHistoryResponse {
  history: UserFilmHistoryRecord[];
  total: number;
}

// Статистика истории просмотров пользователя
export interface UserFilmHistoryStats {
  total_visits: number;
  visits_7d: number;
  visits_30d: number;
  favorite_genre?: string | null;
  favorite_genre_count: number;
}

// Данные для создания рейтинга фильма пользователем
export interface UserFilmRatingCreate {
  rating: number; // [1, 10]
  film_id: number;
}

// Данные для обновления рейтинга фильма пользователем
export interface UserFilmRatingUpdate {
  rating: number; // [1, 10]
}

// Рейтинг фильма пользователем
export interface UserFilmRating {
  rating: number; // [1, 10]
  id: number;
  user_id: number;
  film_id: number;
  created_at: string;
  updated_at: string;
  film?: Film | null;
}

// Ответ для рейтингов пользователя
export interface UserRatingsResponse {
  items: UserFilmRating[];
  page: number;
  page_size: number;
  total_count: number;
}