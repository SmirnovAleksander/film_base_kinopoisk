// Типы для фильмов
import type { Genre } from './genre.types';
import type { Country } from './country.types';

interface BaseFilm {
  title?: string | null;
  original_title?: string | null;
  description?: string | null;
  full_description?: string | null;
  poster?: string | null;
  year?: number | null;
  tagline?: string | null;
  ru_premiere?: string | null;
  world_premiere?: string | null;
  content_rating?: string | null;
  duration?: string | null;
  rating_kp?: number | null;
  kp_votes_count?: string | null;
  rating_imdb?: number | null;
  imdb_votes_count?: string | null;
  user_rating?: number | null;
  budget?: string | null;
  usa_box_office?: string | null;
  rus_box_office?: string | null;
}

export interface FilmUpdate extends BaseFilm {
  is_family_friendly?: boolean | null;
  user_rating_count?: number | null;
}

export interface FilmCreate extends BaseFilm {
  kinopoisk_id: string;
  is_family_friendly?: boolean | null;
  user_rating_count?: number;
}

export interface Film extends FilmCreate {
  id: number;
  is_family_friendly: boolean;
  user_rating_count: number;
}

export interface FilmWithDetails extends Film {
  genres: Genre[];
  countries: Country[];
}

export interface FilmRecommendation extends Film {
  relevance_score: number;
  genre_matches: number;
  stuff_matches: number;
}

export interface FilmRecommendationsResponse {
  items: FilmRecommendation[];
  total_count: number;
}

export interface FilmSearchResponse {
  items: Film[];
  page: number;
  page_size: number;
  total_count: number;
}

export interface FilmAverageRating {
  average_rating?: number | null;
  total_ratings: number;
  min_rating?: number | null;
  max_rating?: number | null;
}

export interface UserFilmRatingCreate {
  rating: number;
  film_id: number;
}

export interface UserFilmRatingUpdate {
  rating: number;
}

export interface UserFilmRating {
  rating: number;
  id: number;
  user_id: number;
  film_id: number;
  created_at: string;
  updated_at: string;
  film?: Film | null;
}

// Алиасы для совместимости
export type RatingCreate = UserFilmRatingCreate;
export type RatingUpdate = UserFilmRatingUpdate;

export interface UserRatingsResponse {
  items: UserFilmRating[];
  page: number;
  page_size: number;
  total_count: number;
}

export interface RatingOperationResponse {
  rating?: number | null;
  created_at: string;
  updated_at: string;
}

// Параметры поиска и фильтрации фильмов
export interface FilmSearchParams {
  query?: string;
  lang?: string;
  page?: number;
  page_size?: number;
}

export interface FilmFilterParams {
  genre?: string;
  genre_id?: number;
  country?: string;
  country_id?: number;
  year?: number;
  start_year?: number;
  end_year?: number;
  title?: string;
  rating_kp_min?: number;
  rating_kp_max?: number;
  min_rating?: number;
  max_rating?: number;
  lang?: string;
  source?: string;
  page?: number;
  page_size?: number;
}

export * from './genre.types';
export * from './country.types';
export * from './film_details.types';
export * from './film_relations.types';