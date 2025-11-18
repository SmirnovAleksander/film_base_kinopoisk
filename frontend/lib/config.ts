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
  MEDIA: '/media',
  PROFILE: '/profile',
  BOOKMARKS: '/bookmarks',
  POSTERS: (id: string | number) => `/posters/${id}`,
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
    GENRES: {
      LIST: '/admin/genres',
      CREATE: '/admin/genres',
      DETAILS: (id: number) => `/admin/genres/${id}`,
      UPDATE: (id: number) => `/admin/genres/${id}`,
      DELETE: (id: number) => `/admin/genres/${id}`,
    },
    COUNTRIES: {
      LIST: '/admin/countries',
      CREATE: '/admin/countries',
      DETAILS: (id: number) => `/admin/countries/${id}`,
      UPDATE: (id: number) => `/admin/countries/${id}`,
      DELETE: (id: number) => `/admin/countries/${id}`,
    },
    MEDIA: {
      LIST: '/admin/media',
      CREATE: '/admin/media',
      DETAILS: (id: number) => `/admin/media/${id}`,
      UPDATE: (id: number) => `/admin/media/${id}`,
      DELETE: (id: number) => `/admin/media/${id}`,
    },
    USERS: {
      LIST: '/admin/users',
      CREATE: '/admin/users',
      DETAILS: (id: number) => `/admin/users/${id}`,
      UPDATE: (id: number) => `/admin/users/${id}`,
      DELETE: (id: number) => `/admin/users/${id}`,
    },
    SIMILAR_FILMS: {
      LIST: '/admin/similar-films',
      CREATE: '/admin/similar-films',
      DETAILS: (id: number) => `/admin/similar-films/${id}`,
      UPDATE: (id: number) => `/admin/similar-films/${id}`,
      DELETE: (id: number) => `/admin/similar-films/${id}`,
    },
    FILM_STILLS: {
      LIST: '/admin/film-stills',
      CREATE: '/admin/film-stills',
      DETAILS: (id: number) => `/admin/film-stills/${id}`,
      UPDATE: (id: number) => `/admin/film-stills/${id}`,
      DELETE: (id: number) => `/admin/film-stills/${id}`,
    },
    FILM_WATCH_PROVIDERS: {
      LIST: '/admin/film-watch-providers',
      CREATE: '/admin/film-watch-providers',
      DETAILS: (id: number) => `/admin/film-watch-providers/${id}`,
      UPDATE: (id: number) => `/admin/film-watch-providers/${id}`,
      DELETE: (id: number) => `/admin/film-watch-providers/${id}`,
    },
    FILM_GENRES: {
      LIST: '/admin/film-genres',
      CREATE: '/admin/film-genres',
      DETAILS: (id: number) => `/admin/film-genres/${id}`,
      DELETE: (id: number) => `/admin/film-genres/${id}`,
    },
    FILM_COUNTRIES: {
      LIST: '/admin/film-countries',
      CREATE: '/admin/film-countries',
      DETAILS: (id: number) => `/admin/film-countries/${id}`,
      DELETE: (id: number) => `/admin/film-countries/${id}`,
    },
    FILM_STUFF: {
      LIST: '/admin/film-stuff',
      CREATE: '/admin/film-stuff',
      DETAILS: (id: number) => `/admin/film-stuff/${id}`,
      UPDATE: (id: number) => `/admin/film-stuff/${id}`,
      DELETE: (id: number) => `/admin/film-stuff/${id}`,
    },
  },
  HEALTH: '/health',
} as const;