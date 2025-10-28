/**
 * Типы для фильмов
 */

// Фильм
export interface Film {
  id: number;
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

// Фильм с деталями
export interface FilmWithDetails extends Film {
  genres: Genre[];
  countries: Country[];
}

// Жанр
export interface Genre {
  id: number;
  name: string;
}

// Страна
export interface Country {
  id: number;
  name: string;
}

// Участник (актер, режиссер и т.д.)
export interface Stuff {
  id: number;
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

// Кадры фильма
export interface FilmStill {
  id: number;
  picture_id: string;
  original_url: string;
  source: string;
}

// Провайдеры просмотра
export interface FilmWatchProvider {
  id: number;
  name: string;
  url: string;
  logo?: string;
}

// Похожие фильмы
export interface SimilarFilm {
  id: number;
  similar_film_id: string;
  similar_film_title: string;
  similar_film_year?: string;
  similar_film_genres?: string[];
  similar_film_poster?: string;
  similar_film_rating?: string;
}

// Рекомендации фильмов
export interface FilmRecommendation extends Film {
  relevance_score: number;
  genre_matches: number;
  stuff_matches: number;
}