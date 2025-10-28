/**
 * Типы для параметров запросов и схем
 */

import { User } from './user.types';

// Фильтр параметры
export interface FilmFilterParams {
  genre_id?: number;
  country_id?: number;
  start_year?: number;
  end_year?: number;
  title?: string;
  lang?: string; // 'ru' или 'en'
  source?: string; // 'kp' или 'imdb'
  min_rating?: number;
  max_rating?: number;
  page?: number;
  page_size?: number;
}

// Поиск параметры
export interface FilmSearchParams {
  query: string;
  lang?: string;
  page?: number;
  page_size?: number;
}

// Типы авторизации
export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  confirm_password: string;
  first_name?: string;
  last_name?: string;
  username?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Создать фильм
export interface FilmCreate {
  kinopoisk_id: string;
  title?: string;
  original_title?: string;
  description?: string;
  full_description?: string;
  poster?: string;
  year?: number;
  tagline?: string;
  ru_premiere?: string;
  world_premiere?: string;
  content_rating?: string;
  is_family_friendly: boolean;
  duration?: string;
  rating_kp?: number;
  kp_votes_count?: string;
  rating_imdb?: number;
  imdb_votes_count?: string;
  budget?: string;
  usa_box_office?: string;
  rus_box_office?: string;
}

// Обновить фильм
export interface FilmUpdate extends Partial<FilmCreate> {}

// Создать участника
export interface StuffCreate {
  kinopoisk_id: string;
  name?: string;
  original_name?: string;
  career?: string[];
  ganres?: string[];
  height?: string;
  birthday_day_month?: string;
  zodiac?: string;
  age?: number;
  birthplace?: string[];
  spouse?: string[];
  children?: string[];
  total_films?: number;
  career_start_year?: number;
  career_end_year?: number;
  image?: string;
}

// Обновить участника
export interface StuffUpdate extends Partial<StuffCreate> {}

// Создать комментарий (повторно экспортируем из interactions)
export type { CommentCreate, CommentUpdate } from './interactions.types';

// Создать рейтинг (повторно экспортируем из interactions)
export type { RatingCreate, RatingUpdate } from './interactions.types';