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
  is_family_friendly?: boolean;
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

export interface Country {
  name: string;
  id: number;
}