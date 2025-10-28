import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  loading: boolean;
  
  // Действия
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: false,
  loading: false,

  toggleSidebar: () => {
    set((state) => ({ sidebarOpen: !state.sidebarOpen }));
  },

  setSidebarOpen: (open: boolean) => {
    set({ sidebarOpen: open });
  },

  setLoading: (loading: boolean) => {
    set({ loading });
  },
}));