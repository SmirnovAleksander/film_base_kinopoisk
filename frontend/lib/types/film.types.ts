// Типы для фильмов

export interface Film {
  kinopoisk_id: string;
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
  is_family_friendly: boolean;
  duration?: string | null;
  rating_kp?: number | null;
  kp_votes_count?: string | null;
  rating_imdb?: number | null;
  imdb_votes_count?: string | null;
  user_rating?: number | null;
  user_rating_count: number;
  budget?: string | null;
  usa_box_office?: string | null;
  rus_box_office?: string | null;
  id: number;
}

export interface FilmCreate {
  kinopoisk_id: string;
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
  is_family_friendly?: boolean | null;
  duration?: string | null;
  rating_kp?: number | null;
  kp_votes_count?: string | null;
  rating_imdb?: number | null;
  imdb_votes_count?: string | null;
  user_rating?: number | null;
  user_rating_count?: number;
  budget?: string | null;
  usa_box_office?: string | null;
  rus_box_office?: string | null;
}

export interface FilmUpdate {
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
  is_family_friendly?: boolean | null;
  duration?: string | null;
  rating_kp?: number | null;
  kp_votes_count?: string | null;
  rating_imdb?: number | null;
  imdb_votes_count?: string | null;
  user_rating?: number | null;
  user_rating_count?: number | null;
  budget?: string | null;
  usa_box_office?: string | null;
  rus_box_office?: string | null;
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

export interface FilmWatchProvider {
  id: number;
  name: string;
  url: string;
  logo?: string | null;
}

export interface SimilarFilm {
  id: number;
  similar_film_id: string;
  similar_film_title: string;
  similar_film_year?: string | null;
  similar_film_genres?: string[] | null;
  similar_film_poster?: string | null;
  similar_film_rating?: string | null;
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

export interface Genre {
  name: string;
  id: number;
}

export interface GenreCreate {
  name: string;
}

export interface GenreUpdate {
  name: string;
}

export interface Country {
  name: string;
  id: number;
}

export interface CountryCreate {
  name: string;
}

export interface CountryUpdate {
  name: string;
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

// Новые типы для Stills в формате от Kinopoisk
export interface Still {
  id: string;
  original: string;
}

// Разрешенные типы для film stills
export type FilmStillType = 'stills' | 'wall' | 'shooting' | 'screenshots';

export interface FilmStills {
  stills?: Still[];
  wall?: Still[];
  shooting?: Still[];
  screenshots?: Still[];
}

// Типы для связанных сущностей фильма
export interface FilmStill {
  id: number;
  film_id: number;
  picture_id: string;
  original_url: string;
  source: FilmStillType; // 'stills', 'wall', 'shooting', 'screenshots'
}

export interface FilmStillCreate {
  film_id: number;
  picture_id: string;
  original_url: string;
  source: string;
}

export interface FilmStillUpdate {
  picture_id?: string | null;
  original_url?: string | null;
  source?: string | null;
}

export interface FilmWatchProviderRead {
  id: number;
  film_id: number;
  name: string;
  url: string;
  logo?: string | null;
}

export interface FilmWatchProviderCreate {
  film_id: number;
  name: string;
  url: string;
  logo?: string | null;
}

export interface FilmWatchProviderUpdate {
  film_id?: number | null;
  name?: string | null;
  url?: string | null;
  logo?: string | null;
}

export interface SimilarFilmRead {
  id: number;
  film_id: number;
  similar_film_id: string;
  similar_film_title: string;
  similar_film_year?: string | null;
  similar_film_genres?: string[] | null;
  similar_film_poster?: string | null;
  similar_film_rating?: string | null;
}

export interface SimilarFilmCreate {
  film_id: number;
  similar_film_id: string;
  similar_film_title: string;
  similar_film_year?: string | null;
  similar_film_genres?: string[] | null;
  similar_film_poster?: string | null;
  similar_film_rating?: string | null;
}

export interface SimilarFilmUpdate {
  similar_film_title?: string | null;
  similar_film_year?: string | null;
  similar_film_genres?: string[] | null;
  similar_film_poster?: string | null;
  similar_film_rating?: string | null;
}

export interface FilmGenreRead {
  id: number;
  film_id: number;
  genre_id: number;
}

export interface FilmGenreCreate {
  film_id: number;
  genre_id: number;
}

export interface FilmCountryRead {
  id: number;
  film_id: number;
  country_id: number;
}

export interface FilmCountryCreate {
  film_id: number;
  country_id: number;
}

export interface FilmStuffRead {
  id: number;
  film_id: number;
  stuff_id: number;
  role?: string | null;
}

export interface FilmStuffCreate {
  film_id: number;
  stuff_id: number;
  role?: string | null;
}

export interface FilmStuffUpdate {
  role?: string | null;
}