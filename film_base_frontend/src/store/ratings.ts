import { create } from "zustand";
import { api } from "../lib/api/client";
import { UserRating, FilmAverageRating, UserRatingWithFilm, Paginated } from "../lib/types";

type RatingsState = {
  // Состояние
  loading: boolean;
  error: string | null;
  
  // Методы для работы с рейтингами
  getUserRating: (filmId: number) => Promise<UserRating | null>;
  setUserRating: (filmId: number, rating: number) => Promise<UserRating>;
  updateUserRating: (filmId: number, rating: number) => Promise<UserRating>;
  deleteUserRating: (filmId: number) => Promise<void>;
  getFilmAverageRating: (filmId: number) => Promise<FilmAverageRating>;
  getUserRatings: (userId: number, page?: number, pageSize?: number) => Promise<Paginated<UserRatingWithFilm>>;
};

export const useRatingsStore = create<RatingsState>((set) => ({
  loading: false,
  error: null,

  async getUserRating(filmId: number) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<{ rating: number | null; created_at?: string; updated_at?: string }>(`/ratings/films/${filmId}/rating`);
      
      if (resp.data.rating === null) {
        return null;
      }
      
      return {
        rating: resp.data.rating,
        created_at: resp.data.created_at!,
        updated_at: resp.data.updated_at!
      };
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get user rating" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async setUserRating(filmId: number, rating: number) {
    set({ loading: true, error: null });
    try {
      const resp = await api.post<UserRating>(`/ratings/films/${filmId}/rating`, null, {
        params: { rating }
      });
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to set rating" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async updateUserRating(filmId: number, rating: number) {
    set({ loading: true, error: null });
    try {
      const resp = await api.put<UserRating>(`/ratings/films/${filmId}/rating`, null, {
        params: { rating }
      });
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to update rating" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async deleteUserRating(filmId: number) {
    set({ loading: true, error: null });
    try {
      await api.delete(`/ratings/films/${filmId}/rating`);
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to delete rating" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async getFilmAverageRating(filmId: number) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<FilmAverageRating>(`/ratings/films/${filmId}/rating/average`);
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get average rating" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async getUserRatings(userId: number, page = 1, pageSize = 20) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Paginated<UserRatingWithFilm>>(`/ratings/users/${userId}/ratings`, {
        params: { page, page_size: pageSize }
      });
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get user ratings" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },
}));
