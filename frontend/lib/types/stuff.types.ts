// Типы для участников/актеров
import type { PaginatedResponse } from './common.types';

export interface Stuff {
  id: number;
  kinopoisk_id: string;
  name_ru?: string | null;
  name_en?: string | null;
  career?: string[] | null;
  genres?: string[] | null;
  height?: string | null;
  zodiac?: string | null;
  birth_date?: string | null;
  birth_place?: string[] | null;
  spouse?: string[] | null;
  children?: string[] | null;
  films_total?: number | null;
  career_start?: number | null;
  photo_url?: string | null;
}

export interface StuffImage {
  id: number;
  stuff_id: number;
  picture_id: string;
  image_url: string;
  image_type: string;
}

export interface StuffFilmography {
  id: number;
  stuff_id: number;
  content_id: string;
  title_ru?: string | null;
  title_en?: string | null;
  release_year?: number | null;
  genres?: string | null;
  countries?: string | null;
  poster_url?: string | null;
  rating_kp?: number | null;
  votes_kp?: number | null;
  role?: string | null;
  release_year_start?: number | null;
  release_year_end?: number | null;
}

export interface StuffCreate {
  kinopoisk_id: string;
  name_ru?: string | null;
  name_en?: string | null;
  career?: string[] | null;
  genres?: string[] | null;
  height?: string | null;
  zodiac?: string | null;
  birth_date?: string | null;
  birth_place?: string[] | null;
  spouse?: string[] | null;
  children?: string[] | null;
  films_total?: number | null;
  career_start?: number | null;
  photo_url?: string | null;
}

export interface StuffUpdate {
  name_ru?: string | null;
  name_en?: string | null;
  career?: string[] | null;
  genres?: string[] | null;
  height?: string | null;
  zodiac?: string | null;
  birth_date?: string | null;
  birth_place?: string[] | null;
  spouse?: string[] | null;
  children?: string[] | null;
  films_total?: number | null;
  career_start?: number | null;
  photo_url?: string | null;
}

export type StuffResponse = PaginatedResponse<Stuff>;