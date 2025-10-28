/**
 * TypeScript типы для API
 */

// Пользователь (соответствует fastapi-users BaseUser схеме)
export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  is_superuser: boolean;
}

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

// Закладка
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

// Media контент
export interface Media {
  id: number;
  url: string;
  title: string;
  image?: string;
  category?: string;
  date?: string;
  comments_count: number;
  card_type?: string;
  type: string;
  parsed_at: string;
}

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
  items: FilmRecommendation[];
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