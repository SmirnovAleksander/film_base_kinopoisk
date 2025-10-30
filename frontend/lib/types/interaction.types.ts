// Типы для закладок, рейтингов, комментариев и истории просмотров

import type { Film } from './film.types';

// ========== ЗАКЛАДКИ ==========

// Запись закладки
export interface Bookmark {
  film_id: number;
  id: number;
  user_id: number;
  created_at: string;
  film?: Film | null;
}

// Ответ для операций с закладками
export interface BookmarkResponse {
  items: Bookmark[];
  page: number;
  page_size: number;
  total_count: number;
}

// Ответ для операций с закладками (операции создания/удаления)
export interface BookmarkOperationResponse {
  status: string;
  bookmark_id?: number | null;
}

// Статус закладки
export interface BookmarkStatusResponse {
  is_bookmarked: boolean;
  bookmark_id?: number | null;
  bookmarked_at?: string | null;
}

// ========== РЕЙТИНГИ ==========

// Данные для создания рейтинга
export interface RatingCreate {
  rating: number; // [1, 10]
  film_id: number;
}

// Данные для обновления рейтинга
export interface RatingUpdate {
  rating: number; // [1, 10]
}

// Ответ для операций с рейтингами
export interface RatingOperationResponse {
  rating?: number | null;
  created_at?: any;
  updated_at?: any;
}

// ========== КОММЕНТАРИИ ==========

// Комментарий
export interface Comment {
  content: string; // [1, 5000] characters
  id: number;
  user_id: number;
  film_id: number;
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  edited_at?: string | null;
}

// Данные для создания комментария
export interface CommentCreate {
  content: string; // [1, 5000] characters
  film_id: number;
}

// Данные для обновления комментария
export interface CommentUpdate {
  content: string; // [1, 5000] characters
}

// Ответ для операций с комментариями
export interface CommentOperationResponse {
  status: string;
  id?: number | null;
}

// ========== ИСТОРИЯ ПРОСМОТРОВ ==========

// Запись в истории просмотров пользователя
export interface UserFilmHistory {
  visited_at: string;
  film: Film;
}

// Ответ для истории просмотров пользователя
export interface UserFilmHistoryResponse {
  history: UserFilmHistory[];
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

// Общий ответ с сообщением
export interface MessageResponse {
  message: string;
}