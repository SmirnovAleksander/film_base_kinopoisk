/**
 * Типы для пользовательских взаимодействий
 */

import { Film } from './film.types';
import { User } from './user.types';

export interface Bookmark {
  id: number;
  user_id: number;
  film_id: number;
  created_at: string;
  film?: Film;
}

// Закладка статус
export interface BookmarkStatus {
  is_bookmarked: boolean;
  bookmark_id?: number;
  bookmarked_at?: string;
}

// Рейтинг пользователя
export interface UserFilmRating {
  id: number;
  user_id: number;
  film_id: number;
  rating: number; // 1.0 - 10.0
  created_at: string;
  updated_at: string;
  film?: Film;
}

// Средний рейтинг фильма
export interface FilmAverageRating {
  average_rating?: number;
  total_ratings: number;
  min_rating?: number;
  max_rating?: number;
}

// Комментарий
export interface Comment {
  id: number;
  user_id: number;
  film_id: number;
  content: string;
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  edited_at?: string;
  user?: User;
}

// История просмотров
export interface UserFilmHistory {
  id: number;
  user_id: number;
  film_id: number;
  visited_at: string;
  film?: Film;
}

// Создать комментарий
export interface CommentCreate {
  content: string;
  film_id: number;
}

// Обновить комментарий
export interface CommentUpdate {
  content: string;
}

// Создать рейтинг
export interface RatingCreate {
  rating: number; // 1.0 - 10.0
}

// Обновить рейтинг
export interface RatingUpdate {
  rating: number;
}