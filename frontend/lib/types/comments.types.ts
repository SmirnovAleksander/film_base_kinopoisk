export interface CommentCreate {
  content: string;
  content_id: number;
  content_type: string;
}

export interface CommentUpdate {
  content: string;
}

export interface Comment {
  id: number;
  user_id: number;
  content_id: number;
  content_type: string;
  content: string;
  is_edited: boolean;
  is_deleted: boolean;
  created_at: string;
  edited_at?: string | null;
}

export interface CommentOperationResponse {
  status: string;
  id?: number | null;
}