import { apiClient } from './client';
import {
  Stuff,
  StuffListResponse,
} from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client';

export class StuffAPI {
  // Получить список участников
  static async getStuff(
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<StuffListResponse> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.STUFF.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить участника по ID
  static async getStuffById(id: number): Promise<Stuff> {
    const response = await apiClient.get(API_ENDPOINTS.STUFF.DETAILS(id));
    return response.data;
  }

  // Получить участника по Кинопоиск ID
  static async getStuffByKinopoiskId(kinopoiskId: string): Promise<Stuff> {
    const response = await apiClient.get(API_ENDPOINTS.STUFF.KINOPOISK_DETAILS(kinopoiskId));
    return response.data;
  }
}