/**
 * Типы для ответов API и пагинации
 */

import { Film } from './film.types';
import { Stuff } from './film.types';
import { Bookmark } from './interactions.types';
import { UserFilmRating } from './interactions.types';
import { Media } from './media.types';

// API ответы с пагинацией
export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total_count: number;
}

// Фильмы поиск ответ
export interface FilmSearchResponse extends PaginatedResponse<Film> {}

// Фильмы рекомендации ответ
export interface FilmRecommendationsResponse {
  items: Film[];
  total_count: number;
}

// Список закладок ответ
export interface BookmarkResponse extends PaginatedResponse<Bookmark> {}

// Список рейтингов пользователя ответ
export interface UserRatingsResponse extends PaginatedResponse<UserFilmRating> {}

// Операции
export interface OperationResponse {
  status: 'created' | 'updated' | 'deleted' | 'added' | 'removed';
  id?: number;
  message?: string;
}

// Закладка операция ответ
export interface BookmarkOperationResponse {
  status: 'added' | 'removed' | 'already_exists' | 'not_found';
  bookmark_id?: number;
}

// Рейтинг операция ответ
export interface RatingOperationResponse {
  rating?: number;
  created_at?: string;
  updated_at?: string;
}

// Комментарий операция ответ
export interface CommentOperationResponse {
  status: 'created' | 'updated' | 'deleted';
  id: number;
}

// История просмотров ответ
export interface UserFilmHistoryResponse {
  history: Array<{
    visited_at: string;
    film: Film;
  }>;
  total: number;
}

// Статистика истории
export interface UserFilmHistoryStats {
  total_visits: number;
  visits_7d: number;
  visits_30d: number;
  favorite_genre?: string;
  favorite_genre_count: number;
}

// Сообщение ответ
export interface MessageResponse {
  message: string;
}

// Медиа контент ответ
export interface MediaResponse {
  media: Media[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
}

// Категории медиа ответ
export interface MediaCategoriesResponse {
  categories: string[];
}

// Типы медиа ответ
export interface MediaTypesResponse {
  types: string[];
}

// Статистика медиа ответ
export interface MediaStatsResponse {
  total_media: number;
  categories: Record<string, number>;
  card_types: Record<string, number>;
  content_types: Record<string, number>;
}

// Список участников ответ
export interface StuffListResponse {
  items: Stuff[];
  page: number;
  page_size: number;
  total_count: number;
}