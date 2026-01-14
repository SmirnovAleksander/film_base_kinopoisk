import { apiClient } from './client.api';
import type {
  Stuff,
  StuffResponse,
  StuffImage,
  StuffFilmography,
} from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client.api';

export class StuffAPI {
  // Получить список участников
  static async getStuff(
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<StuffResponse> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.STUFF.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Поиск участников по имени
  static async searchStuff(
    query: string,
    lang: string = 'ru',
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<StuffResponse> {
    const params = {
      query,
      lang,
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.STUFF.LIST}/search${buildQueryString(params)}`);
    return response.data;
  }

  // Получить изображения участника
  static async getStuffImages(id: number): Promise<StuffImage[]> {
    const response = await apiClient.get(`${API_ENDPOINTS.STUFF.DETAILS(id)}/images`);
    return response.data;
  }

  // Получить фильмографию участника
  static async getStuffFilmography(id: number): Promise<StuffFilmography[]> {
    const response = await apiClient.get(`${API_ENDPOINTS.STUFF.DETAILS(id)}/filmography`);
    return response.data;
  }

  // Получить детали участника
  static async getStuffDetails(id: number): Promise<Stuff> {
    const response = await apiClient.get(API_ENDPOINTS.STUFF.DETAILS(id));
    return response.data;
  }

  // Получить детали участника по Kinopoisk ID
  static async getStuffByKinopoiskId(kinopoiskId: string): Promise<Stuff> {
    const response = await apiClient.get(API_ENDPOINTS.STUFF.KINOPOISK_DETAILS(kinopoiskId));
    return response.data;
  }
}