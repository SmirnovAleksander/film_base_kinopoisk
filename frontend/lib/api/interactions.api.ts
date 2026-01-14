import { apiClient } from './client.api';
import {
  BookmarkResponse,
  BookmarkStatusResponse,
  BookmarkOperationResponse,
  UserContentRating,
  UserRatingsResponse,
  ContentAverageRating,
  UserContentRatingCreate,
  UserContentRatingUpdate,
  RatingOperationResponse,
  Comment,
  CommentCreate,
  CommentUpdate,
  CommentOperationResponse,
} from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client.api';

export class UserInteractionsAPI {
  // ========== ЗАКЛАДКИ ==========

  // Получить список закладок пользователя
  static async getBookmarks(
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<BookmarkResponse> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.BOOKMARKS.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Добавить в закладки
  static async addBookmark(type: string, id: number): Promise<BookmarkOperationResponse> {
    const response = await apiClient.post(API_ENDPOINTS.BOOKMARKS.ADD(type, id));
    return response.data;
  }

  // Удалить из закладок
  static async removeBookmark(type: string, id: number): Promise<BookmarkOperationResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.BOOKMARKS.REMOVE(type, id));
    return response.data;
  }

  // Проверить статус закладки
  static async getBookmarkStatus(type: string, id: number): Promise<BookmarkStatusResponse> {
    const response = await apiClient.get(API_ENDPOINTS.BOOKMARKS.STATUS(type, id));
    return response.data;
  }

  // ========== РЕЙТИНГИ ==========

  // Получить рейтинг пользователя для контента
  static async getUserRating(type: string, id: number): Promise<RatingOperationResponse> {
    const response = await apiClient.get(API_ENDPOINTS.RATINGS.GET(type, id));
    return response.data;
  }

  // Установить рейтинг для контента
  static async setRating(type: string, id: number, ratingData: UserContentRatingCreate): Promise<RatingOperationResponse> {
    const response = await apiClient.post(API_ENDPOINTS.RATINGS.SET(type, id), ratingData);
    return response.data;
  }

  // Обновить рейтинг для контента
  static async updateRating(type: string, id: number, ratingData: UserContentRatingUpdate): Promise<RatingOperationResponse> {
    const response = await apiClient.put(API_ENDPOINTS.RATINGS.SET(type, id), ratingData);
    return response.data;
  }

  // Удалить рейтинг для контента
  static async deleteRating(type: string, id: number): Promise<void> {
    await apiClient.delete(API_ENDPOINTS.RATINGS.DELETE(type, id));
  }

  // Получить средний рейтинг контента
  static async getAverageRating(type: string, id: number): Promise<ContentAverageRating> {
    const response = await apiClient.get(API_ENDPOINTS.RATINGS.AVERAGE(type, id));
    return response.data;
  }

  // Получить все рейтинги пользователя
  static async getUserRatings(
    userId: number,
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<UserRatingsResponse> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.RATINGS.USER_RATINGS(userId)}${buildQueryString(params)}`);
    return response.data;
  }

  // ========== КОММЕНТАРИИ ==========

  // Получить комментарии к контенту
  static async getComments(type: string, id: number): Promise<Comment[]> {
    const response = await apiClient.get(API_ENDPOINTS.COMMENTS.LIST(type, id));
    return response.data;
  }

  // Добавить комментарий к контенту
  static async addComment(type: string, id: number, commentData: CommentCreate): Promise<CommentOperationResponse> {
    const response = await apiClient.post(API_ENDPOINTS.COMMENTS.ADD(type, id), commentData);
    return response.data;
  }

  // Обновить комментарий (по ID комментария)
  static async updateComment(commentId: number, commentData: CommentUpdate): Promise<CommentOperationResponse> {
    const response = await apiClient.put(API_ENDPOINTS.COMMENTS.UPDATE(commentId), commentData);
    return response.data;
  }

  // Удалить комментарий (по ID комментария)
  static async deleteComment(commentId: number): Promise<CommentOperationResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.COMMENTS.DELETE(commentId));
    return response.data;
  }
}