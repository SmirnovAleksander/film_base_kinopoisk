'use client';

import { useHistoryTracker } from '@/hooks/use-history-tracker';

export function HistoryTracker() {
  useHistoryTracker();
  
  return null; // Этот компонент не рендерит ничего
}