import { apiClient } from './client.api';
import type {
  Media,
  MediaResponse,
  MediaStatsResponse,
  MediaCategoriesResponse,
  MediaTypesResponse,
} from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client.api';

export class MediaAPI {
  // Получить список медиа
  static async getMedia(
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE,
    category?: string,
    type?: string
  ): Promise<MediaResponse> {
    const params = {
      page,
      page_size: pageSize,
      category,
      type,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.MEDIA.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить детали медиа
  static async getMediaDetails(id: number): Promise<Media> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.DETAILS(id));
    return response.data;
  }

  // Получить список категорий
  static async getCategories(): Promise<MediaCategoriesResponse> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.CATEGORIES);
    return response.data;
  }

  // Получить список типов медиа
  static async getMediaTypes(): Promise<MediaTypesResponse> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.TYPES);
    return response.data;
  }

  // Получить статистику медиа
  static async getStats(): Promise<MediaStatsResponse> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.STATS);
    return response.data;
  }
}