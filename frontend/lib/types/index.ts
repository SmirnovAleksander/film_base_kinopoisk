// Экспорт всех типов из модуля types

// Авторизация и пользователи
export * from './auth.types';

// Фильмы и связанные данные
export * from './film.types';

// Пользователи и их взаимодействия с фильмами
export * from './user.types';

// Взаимодействия: закладки, рейтинги, комментарии, история
export * from './interaction.types';

// Медиа контент
export * from './media.types';

// Общие типы: ошибки, пагинация, ответы
export * from './common.types';

// Участники фильмов (актеры, режиссеры и т.д.)
export * from './stuff.types';

// ========== АЛИАСЫ ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ ==========

// Типы для экспорта совместимых с существующим кодом
import type { Film, FilmWithDetails } from './film.types';
import type { User } from './auth.types';
import type { UserFilmRating } from './user.types';
import type { Bookmark, BookmarkResponse, BookmarkStatusResponse, BookmarkOperationResponse } from './interaction.types';
import type { RatingCreate, RatingUpdate, RatingOperationResponse } from './interaction.types';
import type { Comment, CommentCreate, CommentUpdate, CommentOperationResponse } from './interaction.types';
import type { UserFilmHistoryResponse, UserFilmHistoryStats } from './interaction.types';
import type { MessageResponse } from './interaction.types';
import type { FilmAverageRating } from './film.types';
import type { UserRatingsResponse } from './user.types';
import type { PaginatedResponse } from './common.types';
import type { Genre, Country } from './film.types';
import type { SimilarFilm, FilmRecommendation, FilmRecommendationsResponse, FilmSearchResponse, FilmFilterParams, FilmSearchParams } from './film.types';
import type { FilmWatchProvider } from './film.types';
import type { Stuff } from './stuff.types';
import type { StuffListResponse } from './common.types';

// Экспорт алиасов для совместимости с существующим кодом
export type {
  Film,
  FilmWithDetails,
  User,
  UserFilmRating,
  Bookmark,
  BookmarkResponse,
  BookmarkStatusResponse,
  BookmarkOperationResponse,
  RatingCreate,
  RatingUpdate,
  RatingOperationResponse,
  Comment,
  CommentCreate,
  CommentUpdate,
  CommentOperationResponse,
  UserFilmHistoryResponse,
  UserFilmHistoryStats,
  MessageResponse,
  FilmAverageRating,
  UserRatingsResponse,
  PaginatedResponse,
  Genre,
  Country,
  SimilarFilm,
  FilmRecommendation,
  FilmRecommendationsResponse,
  FilmSearchResponse,
  FilmFilterParams,
  FilmSearchParams,
  FilmWatchProvider,
  Stuff,
  StuffListResponse,
};