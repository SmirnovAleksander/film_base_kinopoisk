// Типы для закладок

export interface Bookmark {
  film_id: number;
  id: number;
  user_id: number;
  created_at: string;
  film?: Film | null;
}

export interface BookmarkResponse {
  items: Bookmark[];
  page: number;
  page_size: number;
  total_count: number;
}

export interface BookmarkOperationResponse {
  status: string;
  bookmark_id?: number | null;
}

export interface BookmarkStatusResponse {
  is_bookmarked: boolean;
  bookmark_id?: number | null;
  bookmarked_at?: string | null;
}

// Импорт для зависимостей
import type { Film } from './film.types';