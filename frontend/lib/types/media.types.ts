// Типы для медиа контента

export interface Media {
  id: number;
  url?: string | null;
  title?: string | null;
  image_url?: string | null;
  category?: string | null;
  publish_date?: string | null;
  card_type?: string | null;
  type?: string | null;
  parsed_at: string;
}

export interface MediaCreate {
  url?: string | null;
  title?: string | null;
  image_url?: string | null;
  category?: string | null;
  publish_date?: string | null;
  card_type?: string | null;
  type?: string | null;
}

export interface MediaUpdate {
  url?: string | null;
  title?: string | null;
  image_url?: string | null;
  category?: string | null;
  publish_date?: string | null;
  card_type?: string | null;
  type?: string | null;
}

export interface MediaResponse {
  media: Media[];
  pagination: Record<string, any>;
}

export interface MediaStatsResponse {
  total_media: number;
  categories: Record<string, any>;
  card_types: Record<string, any>;
  content_types: Record<string, any>;
}

export interface MediaCategoriesResponse {
  categories: string[];
}

export interface MediaTypesResponse {
  types: string[];
}