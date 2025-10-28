import { create } from 'zustand';
import { FilmsAPI } from '../lib/api/films';
import {
  Film,
  FilmWithDetails,
  Genre,
  Country,
  FilmFilterParams,
  FilmSearchParams,
} from '@/lib/types';
import { PAGINATION } from '../lib/config';

interface FilmsState {
  // Данные
  films: Film[];
  currentFilm: FilmWithDetails | null;
  genres: Genre[];
  countries: Country[];
  
  // Поиск и фильтрация
  searchQuery: string;
  filters: FilmFilterParams;
  isSearching: boolean;
  isLoading: boolean;
  
  // Пагинация
  currentPage: number;
  pageSize: number;
  totalCount: number;
  
  // Действия
  fetchFilms: (page?: number) => Promise<void>;
  searchFilms: (params: FilmSearchParams) => Promise<void>;
  filterFilms: (params: FilmFilterParams) => Promise<void>;
  fetchFilmDetails: (id: number) => Promise<void>;
  fetchGenres: () => Promise<void>;
  fetchCountries: () => Promise<void>;
  setSearchQuery: (query: string) => void;
  setFilters: (filters: Partial<FilmFilterParams>) => void;
  setPage: (page: number) => void;
  clearSearch: () => void;
  clearCurrentFilm: () => void;
  setLoading: (loading: boolean) => void;
}

export const useFilmsStore = create<FilmsState>((set, get) => ({
  // Начальное состояние
  films: [],
  currentFilm: null,
  genres: [],
  countries: [],
  searchQuery: '',
  filters: {},
  isSearching: false,
  isLoading: false,
  currentPage: 1,
  pageSize: PAGINATION.DEFAULT_PAGE_SIZE,
  totalCount: 0,

  // Действия
  fetchFilms: async (page = 1) => {
    set({ isLoading: true, currentPage: page });
    try {
      const response = await FilmsAPI.getFilms(page, get().pageSize);
      set({
        films: response.items,
        totalCount: response.total_count,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  searchFilms: async (params: FilmSearchParams) => {
    set({ isSearching: true, isLoading: true });
    try {
      const response = await FilmsAPI.searchFilms(params);
      set({
        films: response.items,
        totalCount: response.total_count,
        searchQuery: params.query,
        currentPage: params.page || 1,
        isSearching: true,
        isLoading: false,
      });
    } catch (error) {
      set({ isSearching: false, isLoading: false });
      throw error;
    }
  },

  filterFilms: async (params: FilmFilterParams) => {
    set({ isLoading: true });
    try {
      const response = await FilmsAPI.filterFilms(params);
      set({
        films: response.items,
        totalCount: response.total_count,
        filters: params,
        currentPage: params.page || 1,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  fetchFilmDetails: async (id: number) => {
    set({ isLoading: true });
    try {
      const film = await FilmsAPI.getFilmDetails(id);
      set({
        currentFilm: film,
        isLoading: false,
      });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  fetchGenres: async () => {
    try {
      const genres = await FilmsAPI.getGenres();
      set({ genres });
    } catch (error) {
      throw error;
    }
  },

  fetchCountries: async () => {
    try {
      const countries = await FilmsAPI.getCountries();
      set({ countries });
    } catch (error) {
      throw error;
    }
  },

  setSearchQuery: (query: string) => {
    set({ searchQuery: query });
  },

  setFilters: (filters: Partial<FilmFilterParams>) => {
    const currentFilters = get().filters;
    set({ filters: { ...currentFilters, ...filters } });
  },

  setPage: (page: number) => {
    set({ currentPage: page });
  },

  clearSearch: () => {
    set({
      searchQuery: '',
      filters: {},
      isSearching: false,
      currentPage: 1,
    });
  },

  clearCurrentFilm: () => {
    set({ currentFilm: null });
  },

  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },
}));