import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { STORAGE_KEYS } from '../lib/config';

type Theme = 'light' | 'dark' | 'system';

interface UIState {
  theme: Theme;
  sidebarOpen: boolean;
  loading: boolean;
  
  // Действия
  setTheme: (theme: Theme) => void;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setLoading: (loading: boolean) => void;
  getSystemTheme: () => 'light' | 'dark';
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      theme: 'system',
      sidebarOpen: false,
      loading: false,

      setTheme: (theme: Theme) => {
        set({ theme });
        
        // Применяем тему к документу
        if (typeof window !== 'undefined') {
          const root = document.documentElement;
          const systemTheme = get().getSystemTheme();
          const effectiveTheme = theme === 'system' ? systemTheme : theme;
          
          root.classList.remove('light', 'dark');
          root.classList.add(effectiveTheme);
          
          // Сохраняем в localStorage
          localStorage.setItem(STORAGE_KEYS.THEME, theme);
        }
      },

      toggleSidebar: () => {
        set((state) => ({ sidebarOpen: !state.sidebarOpen }));
      },

      setSidebarOpen: (open: boolean) => {
        set({ sidebarOpen: open });
      },

      setLoading: (loading: boolean) => {
        set({ loading });
      },

      getSystemTheme: () => {
        if (typeof window === 'undefined') return 'light';
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      },
    }),
    {
      name: STORAGE_KEYS.THEME,
      partialize: (state) => ({
        theme: state.theme,
      }),
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Применяем тему при загрузке
          state.setTheme(state.theme);
        }
      },
    }
  )
);