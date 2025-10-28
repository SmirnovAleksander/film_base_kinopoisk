/**
 * Конфигурация приложения
 */

// API конфигурация
export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
} as const;

// Роуты приложения
export const ROUTES = {
  HOME: '/',
  LOGIN: '/(auth)/login',
  REGISTER: '/(auth)/register',
  FILMS: '/films',
  FILM_DETAILS: (id: string | number) => `/films/${id}`,
  PROFILE: '/profile',
  BOOKMARKS: '/bookmarks',
  HISTORY: '/history',
} as const;

// Пагинация
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
} as const;

// Фильтры фильмов
export const FILM_FILTERS = {
  DEFAULT_LANG: 'ru' as const,
  DEFAULT_SOURCE: 'kp' as const,
  RATING_MIN: 1,
  RATING_MAX: 10,
} as const;

// Локальное хранилище ключи
export const STORAGE_KEYS = {
  THEME: 'film-base-theme',
  AUTH_TOKEN: 'film-base-token',
  USER_DATA: 'film-base-user',
} as const;

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
  },
  USERS: {
    ME: '/users/me',
    UPDATE: '/users/me',
  },
  FILMS: {
    LIST: '/films',
    SEARCH: '/films/search',
    FILTER: '/films/filter',
    DETAILS: (id: number) => `/films/${id}`,
    RECOMMENDATIONS: (id: number) => `/films/${id}/recommendations`,
    GENRES: '/films/genres',
    COUNTRIES: '/films/countries',
    STUFF: (id: number) => `/films/${id}/stuff`,
    STILL: (id: number) => `/films/${id}/stills`,
  },
  BOOKMARKS: {
    LIST: '/bookmarks',
    ADD: (filmId: number) => `/bookmarks/${filmId}`,
    REMOVE: (filmId: number) => `/bookmarks/${filmId}`,
    STATUS: (filmId: number) => `/bookmarks/${filmId}/status`,
  },
  RATINGS: {
    GET: (filmId: number) => `/ratings/films/${filmId}/rating`,
    SET: (filmId: number) => `/ratings/films/${filmId}/rating`,
    DELETE: (filmId: number) => `/ratings/films/${filmId}/rating`,
    AVERAGE: (filmId: number) => `/ratings/films/${filmId}/rating/average`,
  },
  COMMENTS: {
    LIST: (filmId: number) => `/comments/${filmId}`,
    ADD: (filmId: number) => `/comments/${filmId}`,
    UPDATE: (commentId: number) => `/comments/${commentId}`,
    DELETE: (commentId: number) => `/comments/${commentId}`,
  },
} as const;