// Типы для медиа контента

// Медиа объект
export interface Media {
  url: string; // ≤ 500 characters
  title: string; // ≤ 1000 characters
  image?: string | null;
  category?: string | null;
  date?: string | null;
  comments_count: number;
  card_type?: string | null;
  type: string; // ≤ 20 characters
  id: number;
  parsed_at: string;
}

// Ответ для списка медиа
export interface MediaResponse {
  media: Media[];
  pagination: object;
}

// Ответ для категорий медиа
export interface MediaCategoriesResponse {
  categories: string[];
}

// Ответ для типов медиа
export interface MediaTypesResponse {
  types: string[];
}

// Статистика медиа
export interface MediaStatsResponse {
  total_media: number;
  categories: object;
  card_types: object;
  content_types: object;
}