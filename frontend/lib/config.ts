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
  SERIES: '/series',
  SERIES_DETAILS: (id: string | number) => `/series/${id}`,
  STUFF: '/stuff',
  STUFF_DETAILS: (id: string | number) => `/stuff/${id}`,
  MEDIA: '/media',
  PROFILE: '/profile',
  HISTORY: '/history',
  BOOKMARKS: '/bookmarks',
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
  SERIES: {
    LIST: '/series',
    SEARCH: '/series/search',
    DETAILS: (id: number) => `/series/${id}`,
    STUFF: (id: number) => `/series/${id}/stuff`,
    STILL: (id: number) => `/series/${id}/stills`,
    WATCH_PROVIDERS: (id: number) => `/series/${id}/watch-providers`,
    SIMILAR: (id: number) => `/series/${id}/similar`,
  },
  BOOKMARKS: {
    LIST: '/bookmarks',
    ADD: (type: string, id: number) => `/bookmarks/${type}/${id}`,
    REMOVE: (type: string, id: number) => `/bookmarks/${type}/${id}`,
    STATUS: (type: string, id: number) => `/bookmarks/${type}/${id}/status`,
  },
  RATINGS: {
    GET: (type: string, id: number) => `/ratings/${type}/${id}`,
    SET: (type: string, id: number) => `/ratings/${type}/${id}`,
    DELETE: (type: string, id: number) => `/ratings/${type}/${id}`,
    AVERAGE: (type: string, id: number) => `/ratings/${type}/${id}/average`,
    USER_RATINGS: (userId: number) => `/ratings/users/${userId}/ratings`,
  },
  COMMENTS: {
    LIST: (type: string, id: number) => `/comments/${type}/${id}`,
    ADD: (type: string, id: number) => `/comments/${type}/${id}`,
    UPDATE: (id: number) => `/comments/${id}`,
    DELETE: (id: number) => `/comments/${id}`,
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
    SERIES: {
      LIST: '/admin/series',
      CREATE: '/admin/series',
      DETAILS: (id: number) => `/admin/series/${id}`,
      UPDATE: (id: number) => `/admin/series/${id}`,
      DELETE: (id: number) => `/admin/series/${id}`,
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
    CONTENT_IMAGES: {
      LIST: '/admin/content-images',
      CREATE: '/admin/content-images',
      DETAILS: (id: number) => `/admin/content-images/${id}`,
      DELETE: (id: number) => `/admin/content-images/${id}`,
    },
    CONTENT_WATCH_PROVIDERS: {
      LIST: '/admin/content-watch-providers',
      CREATE: '/admin/content-watch-providers',
      DETAILS: (id: number) => `/admin/content-watch-providers/${id}`,
      DELETE: (id: number) => `/admin/content-watch-providers/${id}`,
    },
    SIMILAR_CONTENT: {
      LIST: '/admin/similar-content',
      CREATE: '/admin/similar-content',
      DETAILS: (id: number) => `/admin/similar-content/${id}`,
      DELETE: (id: number) => `/admin/similar-content/${id}`,
    },
    CONTENT_GENRES: {
      LIST: '/admin/content-genres',
      CREATE: '/admin/content-genres',
      DETAILS: (id: number) => `/admin/content-genres/${id}`,
      DELETE: (id: number) => `/admin/content-genres/${id}`,
    },
    CONTENT_COUNTRIES: {
      LIST: '/admin/content-countries',
      CREATE: '/admin/content-countries',
      DETAILS: (id: number) => `/admin/content-countries/${id}`,
      DELETE: (id: number) => `/admin/content-countries/${id}`,
    },
    CONTENT_STUFF: {
      LIST: '/admin/content-stuff',
      CREATE: '/admin/content-stuff',
      DETAILS: (id: number) => `/admin/content-stuff/${id}`,
      DELETE: (id: number) => `/admin/content-stuff/${id}`,
    },
  },
  HEALTH: '/health',
} as const;