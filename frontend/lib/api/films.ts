import { apiClient } from './client';
import {
  Film,
  FilmWithDetails,
  Genre,
  Country,
  Stuff,
  FilmStill,
  FilmWatchProvider,
  SimilarFilm,
  FilmRecommendation,
  FilmSearchResponse,
  FilmRecommendationsResponse,
  FilmFilterParams,
  FilmSearchParams,
  PaginatedResponse,
} from '../types/api';
import { API_ENDPOINTS, PAGINATION } from '../config';
import { buildQueryString } from './client';

export class FilmsAPI {
  // Получить список фильмов
  static async getFilms(
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<FilmSearchResponse> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Поиск фильмов
  static async searchFilms(params: FilmSearchParams): Promise<FilmSearchResponse> {
    const queryParams = {
      query: params.query,
      lang: params.lang || 'ru',
      page: params.page || 1,
      page_size: params.page_size || PAGINATION.DEFAULT_PAGE_SIZE,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.SEARCH}${buildQueryString(queryParams)}`);
    return response.data;
  }

  // Фильтрация фильмов
  static async filterFilms(params: FilmFilterParams): Promise<FilmSearchResponse> {
    const queryParams = {
      genre_id: params.genre_id,
      country_id: params.country_id,
      start_year: params.start_year,
      end_year: params.end_year,
      title: params.title,
      lang: params.lang || 'ru',
      source: params.source || 'kp',
      min_rating: params.min_rating,
      max_rating: params.max_rating,
      page: params.page || 1,
      page_size: params.page_size || PAGINATION.DEFAULT_PAGE_SIZE,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.FILTER}${buildQueryString(queryParams)}`);
    return response.data;
  }

  // Получить детали фильма
  static async getFilmDetails(id: number): Promise<FilmWithDetails> {
    const response = await apiClient.get(API_ENDPOINTS.FILMS.DETAILS(id));
    return response.data;
  }

  // Получить рекомендации для фильма
  static async getFilmRecommendations(
    id: number,
    limit: number = 10
  ): Promise<FilmRecommendationsResponse> {
    const params = {
      limit,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.RECOMMENDATIONS(id)}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить список жанров
  static async getGenres(): Promise<Genre[]> {
    const response = await apiClient.get(API_ENDPOINTS.FILMS.GENRES);
    return response.data;
  }

  // Получить список стран
  static async getCountries(): Promise<Country[]> {
    const response = await apiClient.get(API_ENDPOINTS.FILMS.COUNTRIES);
    return response.data;
  }

  // Получить участников фильма
  static async getFilmStuff(
    id: number,
    role: string = 'all'
  ): Promise<Stuff[]> {
    const params = {
      role,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.STUFF(id)}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить кадры фильма
  static async getFilmStills(id: number): Promise<{ stills: any[]; wall: any[] }> {
    const response = await apiClient.get(API_ENDPOINTS.FILMS.STILL(id));
    return response.data;
  }

  // Получить провайдеры для просмотра фильма
  static async getFilmWatchProviders(id: number): Promise<FilmWatchProvider[]> {
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.DETAILS(id)}/watch-providers`);
    return response.data;
  }

  // Получить похожие фильмы
  static async getSimilarFilms(id: number): Promise<SimilarFilm[]> {
    const response = await apiClient.get(`${API_ENDPOINTS.FILMS.DETAILS(id)}/similar`);
    return response.data;
  }

  // Получить фильм по Kinopoisk ID
  static async getFilmByKinopoiskId(kinopoiskId: string): Promise<FilmWithDetails> {
    const response = await apiClient.get(API_ENDPOINTS.FILMS.KINOPOISK_DETAILS(kinopoiskId));
    return response.data;
  }
}