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
  LOGIN: '/login',
  REGISTER: '/register',
  FILMS: '/films',
  FILM_DETAILS: (id: string | number) => `/films/${id}`,
  STUFF_DETAILS: (id: string | number) => `/stuff/${id}`,
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
    REQUEST_VERIFY: '/auth/request-verify-token',
    VERIFY: '/auth/verify',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
  },
  USERS: {
    ME: '/users/me',
    UPDATE: '/users/me',
    GET_BY_ID: (id: number) => `/users/${id}`,
    UPDATE_BY_ID: (id: number) => `/users/${id}`,
    DELETE_BY_ID: (id: number) => `/users/${id}`,
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
    WATCH_PROVIDERS: (id: number) => `/films/${id}/watch-providers`,
    SIMILAR: (id: number) => `/films/${id}/similar`,
    KINOPOISK_DETAILS: (kinopoiskId: string) => `/films/kinopoisk/${kinopoiskId}`,
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
    USER_RATINGS: (userId: number) => `/ratings/users/${userId}/ratings`,
  },
  COMMENTS: {
    LIST: (filmId: number) => `/comments/${filmId}`,
    ADD: (filmId: number) => `/comments/${filmId}`,
    UPDATE: (commentId: number) => `/comments/${commentId}`,
    DELETE: (commentId: number) => `/comments/${commentId}`,
  },
  HISTORY: {
    ADD_VISIT: (filmId: number) => `/history/films/${filmId}/visit`,
    LIST: '/history/films',
    CLEAR: '/history/films',
    REMOVE: (filmId: number) => `/history/films/${filmId}`,
    STATS: '/history/films/stats',
  },
  MEDIA: {
    LIST: '/media',
    DETAILS: (id: number) => `/media/${id}`,
    CATEGORIES: '/media/categories',
    TYPES: '/media/types',
    STATS: '/media/stats',
  },
  STUFF: {
    LIST: '/stuff',
    DETAILS: (id: number) => `/stuff/${id}`,
    KINOPOISK_DETAILS: (kinopoiskId: string) => `/stuff/kinopoisk/${kinopoiskId}`,
  },
  ADMIN: {
    FILMS: {
      LIST: '/admin/films',
      CREATE: '/admin/films',
      DETAILS: (id: number) => `/admin/films/${id}`,
      UPDATE: (id: number) => `/admin/films/${id}`,
      DELETE: (id: number) => `/admin/films/${id}`,
    },
    STUFF: {
      LIST: '/admin/stuff',
      CREATE: '/admin/stuff',
      DETAILS: (id: number) => `/admin/stuff/${id}`,
      UPDATE: (id: number) => `/admin/stuff/${id}`,
      DELETE: (id: number) => `/admin/stuff/${id}`,
    },
  },
  // Дополнительные endpoint'ы (необязательные)
  HEALTH: '/health',
} as const;