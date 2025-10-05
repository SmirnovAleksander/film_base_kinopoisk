import { create } from "zustand";
import { api } from "../lib/api/client";
import { Actor, Paginated } from "../lib/types";

type ActorsState = {
  // Состояние
  loading: boolean;
  error: string | null;
  
  // Методы для работы с актерами
  getById: (id: number) => Promise<Actor>;
  getByKinopoiskId: (kinopoiskId: string) => Promise<Actor>;
  list: (page?: number, pageSize?: number) => Promise<Paginated<Actor>>;
};

export const useActorsStore = create<ActorsState>((set) => ({
  loading: false,
  error: null,

  async getById(id: number) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Actor>(`/stuff/${id}`);
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get actor" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async getByKinopoiskId(kinopoiskId: string) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Actor>(`/stuff/kinopoisk/${kinopoiskId}`);
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get actor by Kinopoisk ID" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },

  async list(page = 1, pageSize = 20) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Paginated<Actor>>("/stuff", {
        params: { page, page_size: pageSize },
      });
      return resp.data;
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Failed to get actors list" });
      throw e;
    } finally {
      set({ loading: false });
    }
  },
}));
