import { apiClient } from './client';
import {
  Media,
  MediaResponse,
  MediaCategoriesResponse,
  MediaTypesResponse,
  MediaStatsResponse,
} from '../types/api';
import { API_ENDPOINTS, PAGINATION } from '../config';
import { buildQueryString } from './client';

export class MediaAPI {
  // Получить список медиа контента
  static async getMedia(
    page: number = 1,
    limit: number = PAGINATION.DEFAULT_PAGE_SIZE,
    category?: string,
    cardType?: string,
    contentType?: string
  ): Promise<MediaResponse> {
    const params = {
      page,
      limit,
      category,
      card_type: cardType,
      content_type: contentType,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.MEDIA.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Получить медиа по ID
  static async getMediaById(id: number): Promise<Media> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.DETAILS(id));
    return response.data;
  }

  // Получить список категорий медиа
  static async getMediaCategories(): Promise<MediaCategoriesResponse> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.CATEGORIES);
    return response.data;
  }

  // Получить список типов медиа
  static async getMediaTypes(): Promise<MediaTypesResponse> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.TYPES);
    return response.data;
  }

  // Получить статистику медиа
  static async getMediaStats(): Promise<MediaStatsResponse> {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.STATS);
    return response.data;
  }
}