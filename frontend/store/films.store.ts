import { create } from 'zustand';
import { FilmsAPI } from '@/lib/api';
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
  
  // Категории фильмов
  highRatedFilms: Film[];
  russianFilms: Film[];
  usaFilms: Film[];
  
  // Поиск и фильтрация
  searchQuery: string;
  filters: FilmFilterParams;
  isSearching: boolean;
  isLoading: boolean;
  
  // Состояния загрузки категорий
  isLoadingHighRated: boolean;
  isLoadingRussian: boolean;
  isLoadingUSA: boolean;
  
  // Пагинация
  currentPage: number;
  pageSize: number;
  totalCount: number;
  
  // Действия
  fetchFilms: (page?: number) => Promise<void>;
  searchFilms: (params: FilmSearchParams) => Promise<void>;
  filterFilms: (params: FilmFilterParams, saveTo?: 'highRated' | 'russian' | 'usa' | 'default') => Promise<void>;
  fetchFilmDetails: (id: number) => Promise<void>;
  fetchGenres: () => Promise<void>;
  fetchCountries: () => Promise<void>;
  // Категории фильмов
  fetchHighRatedFilms: (page?: number) => Promise<void>;
  fetchRussianFilms: (page?: number) => Promise<void>;
  fetchUSAFilms: (page?: number) => Promise<void>;
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
  // Категории фильмов
  highRatedFilms: [],
  russianFilms: [],
  usaFilms: [],
  searchQuery: '',
  filters: {},
  isSearching: false,
  isLoading: false,
  // Состояния загрузки категорий
  isLoadingHighRated: false,
  isLoadingRussian: false,
  isLoadingUSA: false,
  currentPage: 1,
  pageSize: PAGINATION.DEFAULT_PAGE_SIZE,
  totalCount: 0,

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

  filterFilms: async (params: FilmFilterParams, saveTo?: 'highRated' | 'russian' | 'usa' | 'default') => {
    const isCategoryRequest = saveTo && saveTo !== 'default';
    
    if (isCategoryRequest) {
      if (saveTo === 'highRated') set({ isLoadingHighRated: true });
      if (saveTo === 'russian') set({ isLoadingRussian: true });
      if (saveTo === 'usa') set({ isLoadingUSA: true });
    } else {
      set({ isLoading: true });
    }
    
    try {
      const response = await FilmsAPI.filterFilms(params);
      
      if (isCategoryRequest) {
        if (saveTo === 'highRated') {
          set({
            highRatedFilms: response.items,
            isLoadingHighRated: false
          });
        }
        if (saveTo === 'russian') {
          set({
            russianFilms: response.items,
            isLoadingRussian: false
          });
        }
        if (saveTo === 'usa') {
          set({
            usaFilms: response.items,
            isLoadingUSA: false
          });
        }
      } else {
        set({
          films: response.items,
          totalCount: response.total_count,
          filters: {
            genre: params.genre,
            genre_id: params.genre_id,
            country: params.country,
            country_id: params.country_id,
            year: params.year,
            start_year: params.start_year,
            end_year: params.end_year,
            title: params.title,
            rating_kp_min: params.rating_kp_min,
            rating_kp_max: params.rating_kp_max,
            min_rating: params.min_rating,
            max_rating: params.max_rating,
            lang: params.lang,
            source: params.source,
            page: params.page,
            page_size: params.page_size,
          },
          currentPage: params.page || 1,
          isLoading: false,
        });
      }
    } catch (error) {
      if (isCategoryRequest) {
        if (saveTo === 'highRated') set({ isLoadingHighRated: false });
        if (saveTo === 'russian') set({ isLoadingRussian: false });
        if (saveTo === 'usa') set({ isLoadingUSA: false });
      } else {
        set({ isLoading: false });
      }
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

  fetchHighRatedFilms: async (page = 1) => {
    await get().filterFilms({
      min_rating: 8,
      max_rating: 10,
      lang: 'ru',
      source: 'kp',
      page,
      page_size: 6,
    }, 'highRated');
  },

  fetchRussianFilms: async (page = 1) => {
    const { countries } = get();
    if (countries.length === 0) {
      await get().fetchCountries();
    }
    
    const updatedCountries = countries.length > 0 ? countries : get().countries;
    const russiaCountry = updatedCountries.find(
      country =>
        country.name.toLowerCase().includes('россия')
    );

    await get().filterFilms({
      country_id: russiaCountry?.id,
      lang: 'ru',
      source: 'kp',
      page,
      page_size: 6,
    }, 'russian');
  },

  fetchUSAFilms: async (page = 1) => {
    const { countries } = get();
    if (countries.length === 0) {
      await get().fetchCountries();
    }
    
    const updatedCountries = countries.length > 0 ? countries : get().countries;
    const usaCountry = updatedCountries.find(
      country =>
        country.name.toLowerCase().includes('сша')
    );

    await get().filterFilms({
      country_id: usaCountry?.id,
      lang: 'ru',
      source: 'kp',
      page,
      page_size: 6,
    }, 'usa');
  },
}));