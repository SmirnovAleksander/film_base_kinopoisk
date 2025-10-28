import { apiClient } from './client';
import {
  UserFilmHistory,
  UserFilmHistoryResponse,
  UserFilmHistoryStats,
  MessageResponse,
} from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client';

export class HistoryAPI {
  // Добавить фильм в историю посещений
  static async addFilmToHistory(filmId: number): Promise<MessageResponse> {
    const response = await apiClient.post(API_ENDPOINTS.HISTORY.ADD_VISIT(filmId));
    return response.data;
  }

  // Получить историю посещений пользователя
  static async getUserHistory(
    limit: number = 10
  ): Promise<UserFilmHistoryResponse> {
    const params = {
      limit,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.HISTORY.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Очистить всю историю
  static async clearHistory(): Promise<MessageResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.HISTORY.CLEAR);
    return response.data;
  }

  // Удалить конкретный фильм из истории
  static async removeFilmFromHistory(filmId: number): Promise<MessageResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.HISTORY.REMOVE(filmId));
    return response.data;
  }

  // Получить статистику истории
  static async getHistoryStats(): Promise<UserFilmHistoryStats> {
    const response = await apiClient.get(API_ENDPOINTS.HISTORY.STATS);
    return response.data;
  }
}