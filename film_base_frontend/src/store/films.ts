import { create } from "zustand";
import api from "@/lib/api/client";
import { FilmListItem, Paginated, FilmDetails } from "@/lib/types";

type FilmsState = {
  items: FilmListItem[];
  page: number;
  pageSize: number;
  totalKnown?: number; // бэкенд пока не отдает total
  loading: boolean;
  error: string | null;
  query: string;
  list: (page?: number, pageSize?: number) => Promise<void>;
  search: (query: string, page?: number, pageSize?: number) => Promise<void>;
  filter: (params: Record<string, any>) => Promise<void>;
  getById: (id: number) => Promise<FilmDetails>;
};

export const useFilmsStore = create<FilmsState>((set, get) => ({
  items: [],
  page: 1,
  pageSize: 20,
  loading: false,
  error: null,
  query: "",
  async list(page = 1, pageSize = 20) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Paginated<FilmListItem>>("/films", {
        params: { page, page_size: pageSize },
      });
      set({ items: resp.data.items, page: resp.data.page, pageSize: resp.data.page_size, loading: false });
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Load error" });
    }
  },
  async search(query, page = 1, pageSize = 20) {
    set({ loading: true, error: null, query });
    try {
      const resp = await api.get<Paginated<FilmListItem>>("/films/search", {
        params: { query, lang: "ru", page, page_size: pageSize },
      });
      set({ items: resp.data.items, page: resp.data.page, pageSize: resp.data.page_size, loading: false });
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Search error" });
    }
  },
  async filter(params) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<Paginated<FilmListItem>>("/films/filter", { params });
      set({ items: resp.data.items, page: resp.data.page, pageSize: resp.data.page_size, loading: false });
    } catch (e: any) {
      set({ loading: false, error: e?.response?.data?.detail || "Filter error" });
    }
  },
  async getById(id: number) {
    const resp = await api.get<FilmDetails>(`/films/${id}`);
    return resp.data;
  },
}));


