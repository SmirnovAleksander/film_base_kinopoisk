import type { Film } from './film.types';
import type { Series } from './series.types';
import type { PaginatedResponse } from './common.types';

export interface Bookmark {
  id: number;
  user_id: number;
  content_id: number;
  content_type: string;
  created_at: string;
  film?: Film | null;
  series?: Series | null;
}

export type BookmarkResponse = PaginatedResponse<Bookmark>;

export interface BookmarkOperationResponse {
  status: string;
  bookmark_id?: number | null;
}

export interface BookmarkStatusResponse {
  is_bookmarked: boolean;
  bookmark_id?: number | null;
  bookmarked_at?: string | null;
}

export interface BookmarkCreate {
  content_id: number;
  content_type: string;
}