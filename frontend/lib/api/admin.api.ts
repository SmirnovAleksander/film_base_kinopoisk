import { apiClient } from './client.api';
import {
  Film,
  Stuff,
  Genre,
  Country,
  Media,
} from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client.api';

export class AdminAPI {
  // ========== УПРАВЛЕНИЕ ФИЛЬМАМИ ==========
  
  // Создать фильм
  static async createFilm(filmData: any): Promise<Film> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILMS.CREATE, filmData);
    return response.data;
  }

  // Получить список всех фильмов
  static async getAllFilms(
    page: number = 1,
    pageSize: number = 50
  ): Promise<Film[]> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILMS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить фильм по ID
  static async getFilmById(id: number): Promise<Film> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILMS.DETAILS(id));
    return response.data;
  }

  // Обновить фильм
  static async updateFilm(id: number, filmData: any): Promise<Film> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILMS.UPDATE(id), filmData);
    return response.data;
  }

  // Удалить фильм
  static async deleteFilm(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILMS.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ УЧАСТНИКАМИ ==========
  
  // Создать участника
  static async createStuff(stuffData: any): Promise<Stuff> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.STUFF.CREATE, stuffData);
    return response.data;
  }

  // Получить список всех участников
  static async getAllStuff(
    page: number = 1,
    pageSize: number = 50
  ): Promise<any> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.STUFF.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить участника по ID
  static async getStuffById(id: number): Promise<Stuff> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.STUFF.DETAILS(id));
    return response.data;
  }

  // Обновить участника
  static async updateStuff(id: number, stuffData: any): Promise<Stuff> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.STUFF.UPDATE(id), stuffData);
    return response.data;
  }

  // Удалить участника
  static async deleteStuff(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.STUFF.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ ЖАНРАМИ ==========
  
  // Создать жанр
  static async createGenre(genreData: { name: string }): Promise<Genre> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.GENRES.CREATE, genreData);
    return response.data;
  }

  // Получить список всех жанров
  static async getAllGenres(): Promise<Genre[]> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.GENRES.LIST);
    return response.data;
  }

  // Получить жанр по ID
  static async getGenreById(id: number): Promise<Genre> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.GENRES.DETAILS(id));
    return response.data;
  }

  // Обновить жанр
  static async updateGenre(id: number, genreData: { name: string }): Promise<Genre> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.GENRES.UPDATE(id), genreData);
    return response.data;
  }

  // Удалить жанр
  static async deleteGenre(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.GENRES.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ СТРАНАМИ ==========
  
  // Создать страну
  static async createCountry(countryData: { name: string }): Promise<Country> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.COUNTRIES.CREATE, countryData);
    return response.data;
  }

  // Получить список всех стран
  static async getAllCountries(): Promise<Country[]> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.COUNTRIES.LIST);
    return response.data;
  }

  // Получить страну по ID
  static async getCountryById(id: number): Promise<Country> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.COUNTRIES.DETAILS(id));
    return response.data;
  }

  // Обновить страну
  static async updateCountry(id: number, countryData: { name: string }): Promise<Country> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.COUNTRIES.UPDATE(id), countryData);
    return response.data;
  }

  // Удалить страну
  static async deleteCountry(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.COUNTRIES.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ МЕДИА ==========
  
  // Создать медиа
  static async createMedia(mediaData: any): Promise<Media> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.MEDIA.CREATE, mediaData);
    return response.data;
  }

  // Получить список всех медиа
  static async getAllMedia(
    page: number = 1,
    pageSize: number = 50
  ): Promise<Media[]> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.MEDIA.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить медиа по ID
  static async getMediaById(id: number): Promise<Media> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.MEDIA.DETAILS(id));
    return response.data;
  }

  // Обновить медиа
  static async updateMedia(id: number, mediaData: any): Promise<Media> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.MEDIA.UPDATE(id), mediaData);
    return response.data;
  }

  // Удалить медиа
  static async deleteMedia(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.MEDIA.DELETE(id));
    return response.data;
  }
}