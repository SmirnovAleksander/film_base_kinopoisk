'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { FilmsAPI } from '@/lib/api';
import {
  Film,
  FilmWithDetails,
  Genre,
  Country,
  Stuff,
  FilmStill,
  FilmWatchProvider,
  SimilarFilm,
  FilmRecommendation,
  FilmRecommendationsResponse,
  FilmSearchResponse,
  FilmFilterParams,
  FilmSearchParams,
} from '@/lib/types';

// Query Keys
export const FILMS_QUERY_KEYS = {
  films: ['films', 'list'],
  filmsPage: (page: number, pageSize: number) => ['films', 'list', 'page', page, pageSize],
  search: (params: FilmSearchParams) => ['films', 'search', params],
  filter: (params: FilmFilterParams) => ['films', 'filter', params],
  film: (id: number) => ['films', 'film', id],
  filmByKinopoiskId: (kinopoiskId: string) => ['films', 'kinopoisk', kinopoiskId],
  genres: ['films', 'genres'],
  countries: ['films', 'countries'],
  filmStuff: (id: number, role?: string) => ['films', id, 'stuff', role],
  filmStills: (id: number) => ['films', id, 'stills'],
  filmWatchProviders: (id: number) => ['films', id, 'watch-providers'],
  similarFilms: (id: number) => ['films', id, 'similar'],
  recommendations: (id: number, limit: number) => ['films', id, 'recommendations', limit],
} as const;

// Хук для получения списка фильмов
export function useFilms(page: number = 1, pageSize: number = 20) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.filmsPage(page, pageSize),
    queryFn: () => FilmsAPI.getFilms(page, pageSize),
    staleTime: 5 * 60 * 1000, // 5 минут
    gcTime: 10 * 60 * 1000, // 10 минут
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

// Хук для поиска фильмов
export function useSearchFilms(params: FilmSearchParams | null) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.search(params!),
    queryFn: () => FilmsAPI.searchFilms(params!),
    enabled: !!params && !!params.query?.trim(),
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    retry: 3,
  });
}

// Хук для фильтрации фильмов
export function useFilterFilms(params: FilmFilterParams | null) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.filter(params!),
    queryFn: () => FilmsAPI.filterFilms(params!),
    enabled: !!params,
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения деталей фильма
export function useFilmDetails(id: number) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.film(id),
    queryFn: () => FilmsAPI.getFilmDetails(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения фильма по Kinopoisk ID
export function useFilmByKinopoiskId(kinopoiskId: string) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.filmByKinopoiskId(kinopoiskId),
    queryFn: () => FilmsAPI.getFilmByKinopoiskId(kinopoiskId),
    enabled: !!kinopoiskId,
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения жанров
export function useGenres() {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.genres,
    queryFn: () => FilmsAPI.getGenres(),
    staleTime: 30 * 60 * 1000, // 30 минут (жанры редко меняются)
    gcTime: 60 * 60 * 1000, // 1 час
    retry: 3,
  });
}

// Хук для получения стран
export function useCountries() {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.countries,
    queryFn: () => FilmsAPI.getCountries(),
    staleTime: 30 * 60 * 1000, // 30 минут
    gcTime: 60 * 60 * 1000, // 1 час
    retry: 3,
  });
}

// Хук для получения участников фильма
export function useFilmStuff(id: number, role: string = 'all') {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.filmStuff(id, role),
    queryFn: () => FilmsAPI.getFilmStuff(id, role),
    enabled: !!id,
    staleTime: 30 * 60 * 1000,
    gcTime: 60 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения кадров фильма
export function useFilmStills(id: number) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.filmStills(id),
    queryFn: () => FilmsAPI.getFilmStills(id),
    enabled: !!id,
    staleTime: 30 * 60 * 1000,
    gcTime: 60 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения провайдеров просмотра
export function useFilmWatchProviders(id: number) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.filmWatchProviders(id),
    queryFn: () => FilmsAPI.getFilmWatchProviders(id),
    enabled: !!id,
    staleTime: 30 * 60 * 1000,
    gcTime: 60 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения похожих фильмов
export function useSimilarFilms(id: number) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.similarFilms(id),
    queryFn: () => FilmsAPI.getSimilarFilms(id),
    enabled: !!id,
    staleTime: 30 * 60 * 1000,
    gcTime: 60 * 60 * 1000,
    retry: 3,
  });
}

// Хук для получения рекомендаций
export function useFilmRecommendations(id: number, limit: number = 10) {
  return useQuery({
    queryKey: FILMS_QUERY_KEYS.recommendations(id, limit),
    queryFn: () => FilmsAPI.getFilmRecommendations(id, limit),
    enabled: !!id,
    staleTime: 10 * 60 * 1000, // 10 минут
    gcTime: 30 * 60 * 1000, // 30 минут
    retry: 3,
  });
}

// Хук для создания нового фильма (админ)
export function useCreateFilm() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (filmData: Partial<Film>) => 
      // Здесь должен быть API вызов для создания фильма
      Promise.reject('Create film API not implemented'),
    onSuccess: () => {
      // Инвалидируем кэш списка фильмов
      queryClient.invalidateQueries({ queryKey: ['films'] });
      console.log('Film created successfully');
    },
    onError: (error) => {
      console.error('Create film error:', error);
    },
  });
}

// Хук для обновления фильма (админ)
export function useUpdateFilm() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Film> }) =>
      // Здесь должен быть API вызов для обновления фильма
      Promise.reject('Update film API not implemented'),
    onSuccess: (_, variables) => {
      // Обновляем кэш конкретного фильма
      queryClient.invalidateQueries({ queryKey: FILMS_QUERY_KEYS.film(variables.id) });
      // Инвалидируем список фильмов
      queryClient.invalidateQueries({ queryKey: ['films'] });
      console.log('Film updated successfully');
    },
    onError: (error) => {
      console.error('Update film error:', error);
    },
  });
}

// Хук для удаления фильма (админ)
export function useDeleteFilm() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) =>
      // Здесь должен быть API вызов для удаления фильма
      Promise.reject('Delete film API not implemented'),
    onSuccess: (_, id) => {
      // Удаляем фильм из кэша
      queryClient.removeQueries({ queryKey: FILMS_QUERY_KEYS.film(id) });
      // Инвалидируем список фильмов
      queryClient.invalidateQueries({ queryKey: ['films'] });
      console.log('Film deleted successfully');
    },
    onError: (error) => {
      console.error('Delete film error:', error);
    },
  });
}

// Хук для создания нового участника (админ)
export function useCreateStuff() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (stuffData: Partial<Stuff>) =>
      // Здесь должен быть API вызов для создания участника
      Promise.reject('Create stuff API not implemented'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['stuff'] });
      console.log('Stuff created successfully');
    },
    onError: (error) => {
      console.error('Create stuff error:', error);
    },
  });
}

// Хук для обновления участника (админ)
export function useUpdateStuff() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Stuff> }) =>
      // Здесь должен быть API вызов для обновления участника
      Promise.reject('Update stuff API not implemented'),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['stuff'] });
      console.log('Stuff updated successfully');
    },
    onError: (error) => {
      console.error('Update stuff error:', error);
    },
  });
}

// Хук для удаления участника (админ)
export function useDeleteStuff() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) =>
      // Здесь должен быть API вызов для удаления участника
      Promise.reject('Delete stuff API not implemented'),
    onSuccess: (_, id) => {
      queryClient.removeQueries({ queryKey: ['stuff', id] });
      queryClient.invalidateQueries({ queryKey: ['stuff'] });
      console.log('Stuff deleted successfully');
    },
    onError: (error) => {
      console.error('Delete stuff error:', error);
    },
  });
}