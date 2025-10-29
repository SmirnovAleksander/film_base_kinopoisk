'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { AuthAPI } from '@/lib/api';
import {
  Bookmark,
  Comment,
  UserFilmRating,
  UserFilmHistory,
  Film,
} from '@/lib/types';

// Query Keys
export const INTERACTIONS_QUERY_KEYS = {
  bookmarks: ['interactions', 'bookmarks'],
  bookmark: (filmId: number) => ['interactions', 'bookmark', filmId],
  bookmarkStatus: (filmId: number) => ['interactions', 'bookmark', filmId, 'status'],
  comments: (filmId: number) => ['interactions', 'comments', filmId],
  comment: (commentId: number) => ['interactions', 'comment', commentId],
  rating: (filmId: number) => ['interactions', 'rating', filmId],
  ratings: (filmId: number) => ['interactions', 'ratings', filmId],
  averageRating: (filmId: number) => ['interactions', 'rating', filmId, 'average'],
  history: ['interactions', 'history'],
  historyStats: ['interactions', 'history', 'stats'],
} as const;

// Хук для получения закладок пользователя
export function useBookmarks() {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.bookmarks,
    queryFn: () => 
      // Здесь должен быть API вызов для получения закладок
      Promise.reject('Get bookmarks API not implemented'),
    staleTime: 5 * 60 * 1000, // 5 минут
    gcTime: 10 * 60 * 1000, // 10 минут
  });
}

// Хук для получения статуса закладки
export function useBookmarkStatus(filmId: number) {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.bookmarkStatus(filmId),
    queryFn: () => 
      // Здесь должен быть API вызов для получения статуса закладки
      Promise.reject('Get bookmark status API not implemented'),
    enabled: !!filmId,
    staleTime: 1 * 60 * 1000, // 1 минута
    gcTime: 5 * 60 * 1000, // 5 минут
  });
}

// Хук для добавления закладки
export function useAddBookmark() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (filmId: number) => 
      // Здесь должен быть API вызов для добавления закладки
      Promise.reject('Add bookmark API not implemented'),
    onSuccess: (_, filmId) => {
      // Обновляем статус закладки в кэше
      queryClient.setQueryData(
        INTERACTIONS_QUERY_KEYS.bookmarkStatus(filmId), 
        true
      );
      
      // Инвалидируем списки закладок
      queryClient.invalidateQueries({ queryKey: INTERACTIONS_QUERY_KEYS.bookmarks });
      queryClient.invalidateQueries({ queryKey: INTERACTIONS_QUERY_KEYS.bookmark(filmId) });
      
      console.log('Bookmark added successfully');
    },
    onError: (error) => {
      console.error('Add bookmark error:', error);
    },
  });
}

// Хук для удаления закладки
export function useRemoveBookmark() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (filmId: number) => 
      // Здесь должен быть API вызов для удаления закладки
      Promise.reject('Remove bookmark API not implemented'),
    onSuccess: (_, filmId) => {
      // Обновляем статус закладки в кэше
      queryClient.setQueryData(
        INTERACTIONS_QUERY_KEYS.bookmarkStatus(filmId), 
        false
      );
      
      // Инвалидируем списки закладок
      queryClient.invalidateQueries({ queryKey: INTERACTIONS_QUERY_KEYS.bookmarks });
      queryClient.invalidateQueries({ queryKey: INTERACTIONS_QUERY_KEYS.bookmark(filmId) });
      
      console.log('Bookmark removed successfully');
    },
    onError: (error) => {
      console.error('Remove bookmark error:', error);
    },
  });
}

// Хук для получения комментариев к фильму
export function useComments(filmId: number) {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.comments(filmId),
    queryFn: () => 
      // Здесь должен быть API вызов для получения комментариев
      Promise.reject('Get comments API not implemented'),
    enabled: !!filmId,
    staleTime: 2 * 60 * 1000, // 2 минуты
    gcTime: 10 * 60 * 1000, // 10 минут
  });
}

// Хук для добавления комментария
export function useAddComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ filmId, content }: { filmId: number; content: string }) => 
      // Здесь должен быть API вызов для добавления комментария
      Promise.reject('Add comment API not implemented'),
    onSuccess: (_, { filmId }) => {
      // Инвалидируем комментарии фильма
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.comments(filmId) 
      });
      console.log('Comment added successfully');
    },
    onError: (error) => {
      console.error('Add comment error:', error);
    },
  });
}

export function useUpdateComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ commentId, content, filmId }: { commentId: number; content: string; filmId: number }) =>
      // Здесь должен быть API вызов для обновления комментария
      Promise.reject('Update comment API not implemented'),
    onSuccess: (_, { filmId }) => {
      // Инвалидируем кэш комментариев конкретного фильма
      queryClient.invalidateQueries({
        queryKey: INTERACTIONS_QUERY_KEYS.comments(filmId)
      });
      console.log('Comment updated successfully');
    },
    onError: (error) => {
      console.error('Update comment error:', error);
    },
  });
}

// Хук для удаления комментария
export function useDeleteComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (commentId: number) => 
      // Здесь должен быть API вызов для удаления комментария
      Promise.reject('Delete comment API not implemented'),
    onSuccess: (_, commentId) => {
      // Удаляем комментарий из кэша
      queryClient.removeQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.comment(commentId) 
      });
      
      // Инвалидируем комментарии
      queryClient.invalidateQueries({ 
        queryKey: ['interactions', 'comments'] 
      });
      
      console.log('Comment deleted successfully');
    },
    onError: (error) => {
      console.error('Delete comment error:', error);
    },
  });
}

// Хук для получения рейтинга пользователя
export function useUserRating(filmId: number) {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.rating(filmId),
    queryFn: () => 
      // Здесь должен быть API вызов для получения рейтинга пользователя
      Promise.reject('Get user rating API not implemented'),
    enabled: !!filmId,
    staleTime: 1 * 60 * 1000, // 1 минута
    gcTime: 5 * 60 * 1000, // 5 минут
  });
}

// Хук для получения среднего рейтинга фильма
export function useAverageRating(filmId: number) {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.averageRating(filmId),
    queryFn: () => 
      // Здесь должен быть API вызов для получения среднего рейтинга
      Promise.reject('Get average rating API not implemented'),
    enabled: !!filmId,
    staleTime: 2 * 60 * 1000, // 2 минуты
    gcTime: 10 * 60 * 1000, // 10 минут
  });
}

// Хук для установки рейтинга
export function useSetRating() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ filmId, rating }: { filmId: number; rating: number }) => 
      // Здесь должен быть API вызов для установки рейтинга
      Promise.reject('Set rating API not implemented'),
    onSuccess: (_, { filmId }) => {
      // Обновляем кэш пользовательского рейтинга
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.rating(filmId) 
      });
      
      // Обновляем кэш среднего рейтинга
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.averageRating(filmId) 
      });
      
      console.log('Rating set successfully');
    },
    onError: (error) => {
      console.error('Set rating error:', error);
    },
  });
}

// Хук для изменения рейтинга
export function useUpdateRating() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ filmId, rating }: { filmId: number; rating: number }) => 
      // Здесь должен быть API вызов для изменения рейтинга
      Promise.reject('Update rating API not implemented'),
    onSuccess: (_, { filmId }) => {
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.rating(filmId) 
      });
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.averageRating(filmId) 
      });
      console.log('Rating updated successfully');
    },
    onError: (error) => {
      console.error('Update rating error:', error);
    },
  });
}

// Хук для удаления рейтинга
export function useDeleteRating() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (filmId: number) => 
      // Здесь должен быть API вызов для удаления рейтинга
      Promise.reject('Delete rating API not implemented'),
    onSuccess: (_, filmId) => {
      // Удаляем рейтинг из кэша
      queryClient.setQueryData(
        INTERACTIONS_QUERY_KEYS.rating(filmId), 
        null
      );
      
      // Инвалидируем средний рейтинг
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.averageRating(filmId) 
      });
      
      console.log('Rating deleted successfully');
    },
    onError: (error) => {
      console.error('Delete rating error:', error);
    },
  });
}

// Хук для получения истории просмотров
export function useHistory() {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.history,
    queryFn: () => 
      // Здесь должен быть API вызов для получения истории
      Promise.reject('Get history API not implemented'),
    staleTime: 2 * 60 * 1000, // 2 минуты
    gcTime: 15 * 60 * 1000, // 15 минут
  });
}

// Хук для получения статистики истории
export function useHistoryStats() {
  return useQuery({
    queryKey: INTERACTIONS_QUERY_KEYS.historyStats,
    queryFn: () => 
      // Здесь должен быть API вызов для получения статистики истории
      Promise.reject('Get history stats API not implemented'),
    staleTime: 5 * 60 * 1000, // 5 минут
    gcTime: 15 * 60 * 1000, // 15 минут
  });
}

// Хук для добавления фильма в историю просмотров
export function useAddToHistory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (filmId: number) => 
      // Здесь должен быть API вызов для добавления в историю
      Promise.reject('Add to history API not implemented'),
    onSuccess: () => {
      // Инвалидируем историю и статистику
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.history 
      });
      queryClient.invalidateQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.historyStats 
      });
      
      console.log('Film added to history successfully');
    },
    onError: (error) => {
      console.error('Add to history error:', error);
    },
  });
}

// Хук для очистки истории просмотров
export function useClearHistory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => 
      // Здесь должен быть API вызов для очистки истории
      Promise.reject('Clear history API not implemented'),
    onSuccess: () => {
      // Очищаем кэш истории
      queryClient.removeQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.history 
      });
      queryClient.removeQueries({ 
        queryKey: INTERACTIONS_QUERY_KEYS.historyStats 
      });
      
      console.log('History cleared successfully');
    },
    onError: (error) => {
      console.error('Clear history error:', error);
    },
  });
}