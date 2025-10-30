// Типы для фильмов и связанных с ними данных

// Базовые типы фильмов
export interface Film {
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
  user_rating?: number;
  user_rating_count: number;
  budget?: string;
  usa_box_office?: string;
  rus_box_office?: string;
}

// Фильм с подробной информацией
export interface FilmWithDetails extends Film {
  id: number;
  genres?: Genre[];
  countries?: Country[];
}

// Фильм с рекомендательной информацией
export interface FilmRecommendation extends FilmWithDetails {
  relevance_score: number;
  genre_matches: number;
  stuff_matches: number;
}

// Похожий фильм
export interface SimilarFilm {
  id: number;
  similar_film_id: string;
  similar_film_title: string;
  similar_film_year?: string;
  similar_film_genres?: string[] | null;
  similar_film_poster?: string | null;
  similar_film_rating?: string | null;
}

// Провайдер для просмотра фильма
export interface FilmWatchProvider {
  id: number;
  name: string;
  url: string;
  logo?: string | null;
}

// Схема для создания фильма
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
  is_family_friendly?: boolean;
  duration?: string;
  rating_kp?: number;
  kp_votes_count?: string;
  rating_imdb?: number;
  imdb_votes_count?: string;
  user_rating?: number;
  user_rating_count?: number;
  budget?: string;
  usa_box_office?: string;
  rus_box_office?: string;
}

// Схема для обновления фильма
export interface FilmUpdate {
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
  is_family_friendly?: boolean;
  duration?: string;
  rating_kp?: number;
  kp_votes_count?: string;
  rating_imdb?: number;
  imdb_votes_count?: string;
  user_rating?: number;
  user_rating_count?: number;
  budget?: string;
  usa_box_office?: string;
  rus_box_office?: string;
}

// Жанр фильма
export interface Genre {
  name: string;
  id: number;
}

// Страна
export interface Country {
  name: string;
  id: number;
}

// Средний рейтинг фильма
export interface FilmAverageRating {
  average_rating?: number | null;
  total_ratings: number;
  min_rating?: number | null;
  max_rating?: number | null;
}

// Поисковый ответ для фильмов
export interface FilmSearchResponse {
  items: Film[];
  page: number;
  page_size: number;
  total_count: number;
}

// Ответ для рекомендаций фильмов
export interface FilmRecommendationsResponse {
  items: FilmRecommendation[];
  total_count: number;
}

// Параметры поиска фильмов
export interface FilmSearchParams {
  query: string;
  lang?: string;
  page?: number;
  page_size?: number;
}

// Параметры фильтрации фильмов
export interface FilmFilterParams {
  genre_id?: number;
  country_id?: number;
  start_year?: number;
  end_year?: number;
  title?: string;
  lang?: string;
  source?: string;
  min_rating?: number;
  max_rating?: number;
  page?: number;
  page_size?: number;
}