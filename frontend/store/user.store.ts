import { create } from 'zustand';
import { UserInteractionsAPI } from '../lib/api/interactions';
import { useAuthStore } from './auth.store';
import {
  Bookmark,
  UserFilmRating,
  Comment,
  BookmarkResponse,
  UserRatingsResponse,
  RatingCreate,
  RatingUpdate,
  CommentCreate,
  CommentUpdate,
} from '../lib/types/api';
import { PAGINATION } from '../lib/config';

interface UserInteractionsState {
  // Закладки
  bookmarks: Bookmark[];
  bookmarkedFilmIds: Set<number>;
  
  // Рейтинги
  userRatings: UserFilmRating[];
  ratedFilmIds: Set<number>;
  
  // Комментарии
  comments: Comment[];
  
  // Состояние загрузки
  isLoadingBookmarks: boolean;
  isLoadingRatings: boolean;
  isLoadingComments: boolean;
  isAddingBookmark: boolean;
  isAddingRating: boolean;
  isAddingComment: boolean;
  
  // Пагинация
  bookmarksPage: number;
  ratingsPage: number;
  bookmarksTotalCount: number;
  ratingsTotalCount: number;

  // Действия для закладок
  fetchBookmarks: (page?: number) => Promise<void>;
  addBookmark: (filmId: number) => Promise<void>;
  removeBookmark: (filmId: number) => Promise<void>;
  checkBookmarkStatus: (filmId: number) => Promise<boolean>;
  clearBookmarks: () => void;
  
  // Действия для рейтингов
  fetchUserRatings: (page?: number) => Promise<void>;
  setFilmRating: (filmId: number, rating: number) => Promise<void>;
  updateFilmRating: (filmId: number, rating: number) => Promise<void>;
  deleteFilmRating: (filmId: number) => Promise<void>;
  getUserRating: (filmId: number) => number | null;
  clearRatings: () => void;
  
  // Действия для комментариев
  fetchFilmComments: (filmId: number) => Promise<void>;
  addComment: (filmId: number, content: string) => Promise<void>;
  updateComment: (commentId: number, content: string) => Promise<void>;
  deleteComment: (commentId: number) => Promise<void>;
  clearComments: () => void;
  
  // Вспомогательные методы
  setBookmarksPage: (page: number) => void;
  setRatingsPage: (page: number) => void;
  setLoadingBookmarks: (loading: boolean) => void;
  setLoadingRatings: (loading: boolean) => void;
  setLoadingComments: (loading: boolean) => void;
}

export const useUserInteractionsStore = create<UserInteractionsState>((set, get) => ({
  // Начальное состояние
  bookmarks: [],
  bookmarkedFilmIds: new Set(),
  userRatings: [],
  ratedFilmIds: new Set(),
  comments: [],
  isLoadingBookmarks: false,
  isLoadingRatings: false,
  isLoadingComments: false,
  isAddingBookmark: false,
  isAddingRating: false,
  isAddingComment: false,
  bookmarksPage: 1,
  ratingsPage: 1,
  bookmarksTotalCount: 0,
  ratingsTotalCount: 0,

  // ========== ЗАКЛАДКИ ==========
  
  fetchBookmarks: async (page = 1) => {
    set({ isLoadingBookmarks: true, bookmarksPage: page });
    try {
      const response = await UserInteractionsAPI.getBookmarks(page, PAGINATION.DEFAULT_PAGE_SIZE);
      const bookmarkedIds = new Set(response.items.map(bookmark => bookmark.film_id));
      
      set({
        bookmarks: response.items,
        bookmarkedFilmIds: bookmarkedIds,
        bookmarksTotalCount: response.total_count,
        isLoadingBookmarks: false,
      });
    } catch (error) {
      set({ isLoadingBookmarks: false });
      throw error;
    }
  },

  addBookmark: async (filmId: number) => {
    set({ isAddingBookmark: true });
    try {
      await UserInteractionsAPI.addBookmark(filmId);
      
      // Обновляем локальное состояние
      const { bookmarkedFilmIds, bookmarks } = get();
      const updatedBookmarkedIds = new Set(bookmarkedFilmIds);
      updatedBookmarkedIds.add(filmId);
      
      // Добавляем закладку в список (можно запросить детали фильма отдельно)
      // Для простоты добавляем только ID, детали можно получить по запросу
      const newBookmark: Bookmark = {
        id: Date.now(), // Временный ID
        user_id: 0,
        film_id: filmId,
        created_at: new Date().toISOString(),
      };
      
      set({
        bookmarkedFilmIds: updatedBookmarkedIds,
        bookmarks: [newBookmark, ...bookmarks],
        isAddingBookmark: false,
      });
    } catch (error) {
      set({ isAddingBookmark: false });
      throw error;
    }
  },

  removeBookmark: async (filmId: number) => {
    set({ isAddingBookmark: true });
    try {
      await UserInteractionsAPI.removeBookmark(filmId);
      
      // Обновляем локальное состояние
      const { bookmarkedFilmIds, bookmarks } = get();
      const updatedBookmarkedIds = new Set(bookmarkedFilmIds);
      updatedBookmarkedIds.delete(filmId);
      
      const updatedBookmarks = bookmarks.filter(bookmark => bookmark.film_id !== filmId);
      
      set({
        bookmarkedFilmIds: updatedBookmarkedIds,
        bookmarks: updatedBookmarks,
        isAddingBookmark: false,
      });
    } catch (error) {
      set({ isAddingBookmark: false });
      throw error;
    }
  },

  checkBookmarkStatus: async (filmId: number): Promise<boolean> => {
    try {
      const status = await UserInteractionsAPI.getBookmarkStatus(filmId);
      return status.is_bookmarked;
    } catch (error) {
      return false;
    }
  },

  clearBookmarks: () => {
    set({
      bookmarks: [],
      bookmarkedFilmIds: new Set(),
      bookmarksTotalCount: 0,
      bookmarksPage: 1,
    });
  },

  // ========== РЕЙТИНГИ ==========
  
  fetchUserRatings: async (page = 1) => {
    set({ isLoadingRatings: true, ratingsPage: page });
    try {
      // Получаем ID текущего пользователя из auth store
      const { user } = useAuthStore.getState();
      if (!user) {
        throw new Error('Пользователь не авторизован');
      }
      
      const response = await UserInteractionsAPI.getUserRatings(user.id, page, PAGINATION.DEFAULT_PAGE_SIZE);
      const ratedIds = new Set(response.items.map(rating => rating.film_id));
      
      set({
        userRatings: response.items,
        ratedFilmIds: ratedIds,
        ratingsTotalCount: response.total_count,
        isLoadingRatings: false,
      });
    } catch (error) {
      set({ isLoadingRatings: false });
      throw error;
    }
  },

  setFilmRating: async (filmId: number, rating: number) => {
    set({ isAddingRating: true });
    try {
      const ratingData: RatingCreate = { rating };
      await UserInteractionsAPI.setFilmRating(filmId, ratingData);
      
      // Обновляем локальное состояние
      const { ratedFilmIds, userRatings } = get();
      const updatedRatedIds = new Set(ratedFilmIds);
      updatedRatedIds.add(filmId);
      
      // Добавляем или обновляем рейтинг в списке
      const existingRatingIndex = userRatings.findIndex(r => r.film_id === filmId);
      if (existingRatingIndex >= 0) {
        userRatings[existingRatingIndex].rating = rating;
        userRatings[existingRatingIndex].updated_at = new Date().toISOString();
      } else {
        const newRating: UserFilmRating = {
          id: Date.now(), // Временный ID
          user_id: 0,
          film_id: filmId,
          rating,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        userRatings.unshift(newRating);
      }
      
      set({
        ratedFilmIds: updatedRatedIds,
        userRatings: [...userRatings],
        isAddingRating: false,
      });
    } catch (error) {
      set({ isAddingRating: false });
      throw error;
    }
  },

  updateFilmRating: async (filmId: number, rating: number) => {
    return get().setFilmRating(filmId, rating);
  },

  deleteFilmRating: async (filmId: number) => {
    set({ isAddingRating: true });
    try {
      await UserInteractionsAPI.deleteFilmRating(filmId);
      
      // Обновляем локальное состояние
      const { ratedFilmIds, userRatings } = get();
      const updatedRatedIds = new Set(ratedFilmIds);
      updatedRatedIds.delete(filmId);
      
      const updatedRatings = userRatings.filter(rating => rating.film_id !== filmId);
      
      set({
        ratedFilmIds: updatedRatedIds,
        userRatings: updatedRatings,
        isAddingRating: false,
      });
    } catch (error) {
      set({ isAddingRating: false });
      throw error;
    }
  },

  getUserRating: (filmId: number): number | null => {
    const { userRatings } = get();
    const rating = userRatings.find(r => r.film_id === filmId);
    return rating ? rating.rating : null;
  },

  clearRatings: () => {
    set({
      userRatings: [],
      ratedFilmIds: new Set(),
      ratingsTotalCount: 0,
      ratingsPage: 1,
    });
  },

  // ========== КОММЕНТАРИИ ==========
  
  fetchFilmComments: async (filmId: number) => {
    set({ isLoadingComments: true });
    try {
      const comments = await UserInteractionsAPI.getFilmComments(filmId);
      set({
        comments,
        isLoadingComments: false,
      });
    } catch (error) {
      set({ isLoadingComments: false });
      throw error;
    }
  },

  addComment: async (filmId: number, content: string) => {
    set({ isAddingComment: true });
    try {
      const commentData: CommentCreate = { content };
      await UserInteractionsAPI.addComment(filmId, commentData);
      
      // Обновляем локальное состояние
      const { comments } = get();
      const newComment: Comment = {
        id: Date.now(), // Временный ID
        user_id: 0,
        film_id: filmId,
        content,
        is_edited: false,
        is_deleted: false,
        created_at: new Date().toISOString(),
      };
      
      set({
        comments: [newComment, ...comments],
        isAddingComment: false,
      });
    } catch (error) {
      set({ isAddingComment: false });
      throw error;
    }
  },

  updateComment: async (commentId: number, content: string) => {
    set({ isAddingComment: true });
    try {
      const commentData: CommentUpdate = { content };
      await UserInteractionsAPI.updateComment(commentId, commentData);
      
      // Обновляем локальное состояние
      const { comments } = get();
      const updatedComments = comments.map(comment => 
        comment.id === commentId 
          ? { ...comment, content, is_edited: true, edited_at: new Date().toISOString() }
          : comment
      );
      
      set({
        comments: updatedComments,
        isAddingComment: false,
      });
    } catch (error) {
      set({ isAddingComment: false });
      throw error;
    }
  },

  deleteComment: async (commentId: number) => {
    set({ isAddingComment: true });
    try {
      await UserInteractionsAPI.deleteComment(commentId);
      
      // Обновляем локальное состояние (мягкое удаление)
      const { comments } = get();
      const updatedComments = comments.map(comment => 
        comment.id === commentId 
          ? { ...comment, is_deleted: true }
          : comment
      );
      
      set({
        comments: updatedComments,
        isAddingComment: false,
      });
    } catch (error) {
      set({ isAddingComment: false });
      throw error;
    }
  },

  clearComments: () => {
    set({
      comments: [],
    });
  },

  // ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
  
  setBookmarksPage: (page: number) => {
    set({ bookmarksPage: page });
  },

  setRatingsPage: (page: number) => {
    set({ ratingsPage: page });
  },

  setLoadingBookmarks: (loading: boolean) => {
    set({ isLoadingBookmarks: loading });
  },

  setLoadingRatings: (loading: boolean) => {
    set({ isLoadingRatings: loading });
  },

  setLoadingComments: (loading: boolean) => {
    set({ isLoadingComments: loading });
  },
}));