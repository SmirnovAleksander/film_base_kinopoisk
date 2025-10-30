// Типы для комментариев

export interface CommentCreate {
  content: string;
  film_id: number;
}

export interface CommentUpdate {
  content: string;
}

export interface Comment {
  content: string;
  id: number;
  user_id: number;
  film_id: number;
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  edited_at?: string | null;
}

export interface CommentOperationResponse {
  status: string;
  id?: number | null;
}