import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface HistoryItem {
    id: number;
    type: 'film' | 'person';
    title: string;
    image?: string | null;
    description?: string;
    visitedAt: string;
}

interface HistoryState {
    items: HistoryItem[];
    addToHistory: (item: Omit<HistoryItem, 'visitedAt'>) => void;
    removeFromHistory: (id: number, type: 'film' | 'person') => void;
    clearHistory: () => void;
}

export const useHistoryStore = create<HistoryState>()(
    persist(
        (set, get) => ({
            items: [],
            addToHistory: (item) => {
                const { items } = get();
                const newItem = { ...item, visitedAt: new Date().toISOString() };
                const filteredItems = items.filter(
                    (i) => !(i.id === item.id && i.type === item.type)
                );
                const newItems = [newItem, ...filteredItems].slice(0, 20);

                set({ items: newItems });
            },
            removeFromHistory: (id, type) => {
                const { items } = get();
                set({
                    items: items.filter((i) => !(i.id === id && i.type === type)),
                });
            },
            clearHistory: () => set({ items: [] }),
        }),
        {
            name: 'film-base-history',
        }
    )
);
