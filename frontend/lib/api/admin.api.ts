import { apiClient } from './client.api';
import {
  Film,
  Stuff,
  Genre,
  Country,
  Media,
  User,
  SimilarFilmRead,
  SimilarFilmCreate,
  SimilarFilmUpdate,
  FilmStill,
  FilmStillCreate,
  FilmStillUpdate,
  FilmWatchProviderRead,
  FilmWatchProviderCreate,
  FilmWatchProviderUpdate,
  FilmGenreRead,
  FilmGenreCreate,
  FilmCountryRead,
  FilmCountryCreate,
  FilmStuffRead,
  FilmStuffCreate,
  FilmStuffUpdate,
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
      page_size: Math.min(pageSize, 100), // Backend ограничивает максимум 100
    };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.STUFF.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить все участники (с пагинацией, если нужно больше 100)
  static async getAllStuffAll(): Promise<Stuff[]> {
    const allStuff: Stuff[] = [];
    let page = 1;
    let hasMore = true;

    while (hasMore) {
      const response = await this.getAllStuff(page, 100);
      // Backend возвращает StuffListResponse с полями items, page, page_size, total_count
      if (response && Array.isArray(response.items)) {
        allStuff.push(...response.items);
        const totalCount = response.total_count || 0;
        hasMore = response.items.length === 100 && totalCount > page * 100;
      } else if (Array.isArray(response)) {
        // Fallback: если ответ - массив напрямую
        allStuff.push(...response);
        hasMore = response.length === 100;
      } else {
        hasMore = false;
      }
      page++;
      
      // Защита от бесконечного цикла
      if (page > 1000) break;
    }

    return allStuff;
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

  // ========== УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ==========
  
  // Создать пользователя
  static async createUser(userData: any): Promise<User> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.USERS.CREATE, userData);
    return response.data;
  }

  // Получить список всех пользователей
  static async getAllUsers(
    page: number = 1,
    pageSize: number = 50
  ): Promise<User[]> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.USERS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить пользователя по ID
  static async getUserById(id: number): Promise<User> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.USERS.DETAILS(id));
    return response.data;
  }

  // Обновить пользователя
  static async updateUser(id: number, userData: any): Promise<User> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.USERS.UPDATE(id), userData);
    return response.data;
  }

  // Удалить пользователя
  static async deleteUser(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.USERS.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ ПОХОЖИМИ ФИЛЬМАМИ ==========
  
  static async createSimilarFilm(data: SimilarFilmCreate): Promise<SimilarFilmRead> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.CREATE, data);
    return response.data;
  }

  static async getAllSimilarFilms(page: number = 1, pageSize: number = 50): Promise<SimilarFilmRead[]> {
    const params = { page, page_size: pageSize };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.SIMILAR_FILMS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  static async getSimilarFilmById(id: number): Promise<SimilarFilmRead> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.DETAILS(id));
    return response.data;
  }

  static async updateSimilarFilm(id: number, data: SimilarFilmUpdate): Promise<SimilarFilmRead> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.UPDATE(id), data);
    return response.data;
  }

  static async deleteSimilarFilm(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ КАДРАМИ ФИЛЬМА ==========
  
  static async createFilmStill(data: FilmStillCreate): Promise<FilmStill> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_STILLS.CREATE, data);
    return response.data;
  }

  static async getAllFilmStills(page: number = 1, pageSize: number = 50): Promise<FilmStill[]> {
    const params = { page, page_size: pageSize };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_STILLS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  static async getFilmStillById(id: number): Promise<FilmStill> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_STILLS.DETAILS(id));
    return response.data;
  }

  static async updateFilmStill(id: number, data: FilmStillUpdate): Promise<FilmStill> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILM_STILLS.UPDATE(id), data);
    return response.data;
  }

  static async deleteFilmStill(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_STILLS.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ ПРОВАЙДЕРАМИ ПРОСМОТРА ==========
  
  static async createFilmWatchProvider(data: FilmWatchProviderCreate): Promise<FilmWatchProviderRead> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.CREATE, data);
    return response.data;
  }

  static async getAllFilmWatchProviders(page: number = 1, pageSize: number = 50): Promise<FilmWatchProviderRead[]> {
    const params = { page, page_size: pageSize };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  static async getFilmWatchProviderById(id: number): Promise<FilmWatchProviderRead> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.DETAILS(id));
    return response.data;
  }

  static async updateFilmWatchProvider(id: number, data: FilmWatchProviderUpdate): Promise<FilmWatchProviderRead> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.UPDATE(id), data);
    return response.data;
  }

  static async deleteFilmWatchProvider(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ ЖАНРАМИ ФИЛЬМА ==========
  
  static async createFilmGenre(data: FilmGenreCreate): Promise<FilmGenreRead> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_GENRES.CREATE, data);
    return response.data;
  }

  static async getAllFilmGenres(page: number = 1, pageSize: number = 50): Promise<FilmGenreRead[]> {
    const params = { page, page_size: pageSize };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_GENRES.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  static async getFilmGenreById(id: number): Promise<FilmGenreRead> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_GENRES.DETAILS(id));
    return response.data;
  }

  static async deleteFilmGenre(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_GENRES.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ СТРАНАМИ ФИЛЬМА ==========
  
  static async createFilmCountry(data: FilmCountryCreate): Promise<FilmCountryRead> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_COUNTRIES.CREATE, data);
    return response.data;
  }

  static async getAllFilmCountries(page: number = 1, pageSize: number = 50): Promise<FilmCountryRead[]> {
    const params = { page, page_size: pageSize };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_COUNTRIES.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  static async getFilmCountryById(id: number): Promise<FilmCountryRead> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_COUNTRIES.DETAILS(id));
    return response.data;
  }

  static async deleteFilmCountry(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_COUNTRIES.DELETE(id));
    return response.data;
  }

  // ========== УПРАВЛЕНИЕ УЧАСТНИКАМИ ФИЛЬМА ==========
  
  static async createFilmStuff(data: FilmStuffCreate): Promise<FilmStuffRead> {
    const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_STUFF.CREATE, data);
    return response.data;
  }

  static async getAllFilmStuff(page: number = 1, pageSize: number = 50): Promise<FilmStuffRead[]> {
    const params = { page, page_size: pageSize };
    const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_STUFF.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  static async getFilmStuffById(id: number): Promise<FilmStuffRead> {
    const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_STUFF.DETAILS(id));
    return response.data;
  }

  static async updateFilmStuff(id: number, data: FilmStuffUpdate): Promise<FilmStuffRead> {
    const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILM_STUFF.UPDATE(id), data);
    return response.data;
  }

  static async deleteFilmStuff(id: number): Promise<any> {
    const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_STUFF.DELETE(id));
    return response.data;
  }
}