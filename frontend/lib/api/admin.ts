import { apiClient } from './client';
import {
  Film,
  Stuff,
} from '../types/api';
import { API_ENDPOINTS, PAGINATION } from '../config';
import { buildQueryString } from './client';

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
}