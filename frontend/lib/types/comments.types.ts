// Типы для комментариев

interface BaseComment {
  content: string;
}

export interface CommentCreate extends BaseComment {
  film_id: number;
}

export interface CommentUpdate extends BaseComment { }

export interface Comment extends BaseComment {
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