import { apiClient } from './client';
import {
  Bookmark,
  BookmarkResponse,
  BookmarkStatus,
  BookmarkOperationResponse,
  UserFilmRating,
  UserRatingsResponse,
  FilmAverageRating,
  RatingCreate,
  RatingUpdate,
  RatingOperationResponse,
  Comment,
  CommentCreate,
  CommentUpdate,
  CommentOperationResponse,
  UserFilmHistoryResponse,
  MessageResponse,
  UserFilmHistoryStats,
} from '../types/api';
import { API_ENDPOINTS, PAGINATION } from '../config';
import { buildQueryString } from './client';

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

  // Добавить фильм в закладки
  static async addBookmark(filmId: number): Promise<BookmarkOperationResponse> {
    const response = await apiClient.post(API_ENDPOINTS.BOOKMARKS.ADD(filmId));
    return response.data;
  }

  // Удалить фильм из закладок
  static async removeBookmark(filmId: number): Promise<BookmarkOperationResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.BOOKMARKS.REMOVE(filmId));
    return response.data;
  }

  // Проверить статус закладки
  static async getBookmarkStatus(filmId: number): Promise<BookmarkStatus> {
    const response = await apiClient.get(API_ENDPOINTS.BOOKMARKS.STATUS(filmId));
    return response.data;
  }

  // ========== РЕЙТИНГИ ==========

  // Получить рейтинг пользователя для фильма
  static async getUserFilmRating(filmId: number): Promise<RatingOperationResponse> {
    const response = await apiClient.get(API_ENDPOINTS.RATINGS.GET(filmId));
    return response.data;
  }

  // Установить рейтинг для фильма
  static async setFilmRating(filmId: number, ratingData: RatingCreate): Promise<RatingOperationResponse> {
    const response = await apiClient.post(API_ENDPOINTS.RATINGS.SET(filmId), ratingData);
    return response.data;
  }

  // Обновить рейтинг для фильма
  static async updateFilmRating(filmId: number, ratingData: RatingUpdate): Promise<RatingOperationResponse> {
    const response = await apiClient.put(API_ENDPOINTS.RATINGS.SET(filmId), ratingData);
    return response.data;
  }

  // Удалить рейтинг для фильма
  static async deleteFilmRating(filmId: number): Promise<void> {
    await apiClient.delete(API_ENDPOINTS.RATINGS.DELETE(filmId));
  }

  // Получить средний рейтинг фильма
  static async getFilmAverageRating(filmId: number): Promise<FilmAverageRating> {
    const response = await apiClient.get(API_ENDPOINTS.RATINGS.AVERAGE(filmId));
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

  // Получить комментарии к фильму
  static async getFilmComments(filmId: number): Promise<Comment[]> {
    const response = await apiClient.get(API_ENDPOINTS.COMMENTS.LIST(filmId));
    return response.data;
  }

  // Добавить комментарий к фильму
  static async addComment(filmId: number, commentData: CommentCreate): Promise<CommentOperationResponse> {
    const response = await apiClient.post(API_ENDPOINTS.COMMENTS.ADD(filmId), commentData);
    return response.data;
  }

  // Обновить комментарий
  static async updateComment(commentId: number, commentData: CommentUpdate): Promise<CommentOperationResponse> {
    const response = await apiClient.put(API_ENDPOINTS.COMMENTS.UPDATE(commentId), commentData);
    return response.data;
  }

  // Удалить комментарий
  static async deleteComment(commentId: number): Promise<CommentOperationResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.COMMENTS.DELETE(commentId));
    return response.data;
  }

  // ========== ИСТОРИЯ ПРОСМОТРОВ ==========

  // Получить историю просмотров пользователя
  static async getUserHistory(
    page: number = 1,
    pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
  ): Promise<UserFilmHistoryResponse> {
    const params = {
      page,
      page_size: pageSize,
    };
    const response = await apiClient.get(`${API_ENDPOINTS.HISTORY.LIST}${buildQueryString(params)}`);
    return response.data;
  }

  // Добавить фильм в историю просмотров
  static async addFilmToHistory(filmId: number): Promise<MessageResponse> {
    const response = await apiClient.post(API_ENDPOINTS.HISTORY.ADD_VISIT(filmId));
    return response.data;
  }

  // Удалить фильм из истории просмотров
  static async removeFilmFromHistory(filmId: number): Promise<MessageResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.HISTORY.REMOVE(filmId));
    return response.data;
  }

  // Очистить всю историю
  static async clearHistory(): Promise<MessageResponse> {
    const response = await apiClient.delete(API_ENDPOINTS.HISTORY.CLEAR);
    return response.data;
  }

  // Получить статистику истории
  static async getHistoryStats(): Promise<UserFilmHistoryStats> {
    const response = await apiClient.get(API_ENDPOINTS.HISTORY.STATS);
    return response.data;
  }
}