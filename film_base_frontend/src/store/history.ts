import { create } from 'zustand';
import { api } from '../lib/api/client';
import { FilmHistoryResponse, HistoryStats } from '../lib/types';

interface HistoryState {
  loading: boolean;
  error: string | null;
  history: FilmHistoryResponse | null;
  stats: HistoryStats | null;

  // Методы
  addFilmToHistory: (filmId: number) => Promise<void>;
  getHistory: (limit?: number) => Promise<FilmHistoryResponse>;
  clearHistory: () => Promise<void>;
  removeFilmFromHistory: (filmId: number) => Promise<void>;
  getHistoryStats: () => Promise<HistoryStats>;
}

export const useHistoryStore = create<HistoryState>((set, get) => ({
  loading: false,
  error: null,
  history: null,
  stats: null,

  async addFilmToHistory(filmId: number) {
    set({ loading: true, error: null });
    try {
      await api.post(`/history/films/${filmId}/visit`);
      // Обновляем историю после добавления
      await get().getHistory();
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Ошибка при добавлении в историю' });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  async getHistory(limit = 10) {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<FilmHistoryResponse>(`/history/films/history?limit=${limit}`);
      set({ history: resp.data });
      return resp.data;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Ошибка при получении истории';
      set({ error: errorMessage });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  async clearHistory() {
    set({ loading: true, error: null });
    try {
      await api.delete('/history/films/history');
      set({ history: null });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Ошибка при очистке истории' });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  async removeFilmFromHistory(filmId: number) {
    set({ loading: true, error: null });
    try {
      await api.delete(`/history/films/${filmId}/history`);
      // Обновляем историю после удаления
      await get().getHistory();
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Ошибка при удалении из истории' });
      throw error;
    } finally {
      set({ loading: false });
    }
  },

  async getHistoryStats() {
    set({ loading: true, error: null });
    try {
      const resp = await api.get<HistoryStats>('/history/films/history/stats');
      set({ stats: resp.data });
      return resp.data;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Ошибка при получении статистики';
      set({ error: errorMessage });
      throw error;
    } finally {
      set({ loading: false });
    }
  },
}));
