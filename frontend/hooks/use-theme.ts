import { useEffect } from 'react';
import { useUIStore } from '../store';

export function useTheme() {
  const {
    theme,
    setTheme,
    getSystemTheme,
  } = useUIStore();

  // Применяем тему при изменении
  useEffect(() => {
    const applyTheme = () => {
      const root = document.documentElement;
      const systemTheme = getSystemTheme();
      const effectiveTheme = theme === 'system' ? systemTheme : theme;
      
      root.classList.remove('light', 'dark');
      root.classList.add(effectiveTheme);
    };

    applyTheme();
  }, [theme, getSystemTheme]);

  // Слушаем изменения системной темы
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = () => {
      if (theme === 'system') {
        const root = document.documentElement;
        const systemTheme = getSystemTheme();
        
        root.classList.remove('light', 'dark');
        root.classList.add(systemTheme);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme, getSystemTheme]);

  return {
    theme,
    setTheme,
    effectiveTheme: theme === 'system' ? getSystemTheme() : theme,
    isDark: (theme === 'system' ? getSystemTheme() : theme) === 'dark',
    isLight: (theme === 'system' ? getSystemTheme() : theme) === 'light',
    isSystem: theme === 'system',
  };
}