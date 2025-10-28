/**
 * Типы для медиа контента
 */

export interface Media {
  id: number;
  url: string;
  title: string;
  image?: string;
  category?: string;
  date?: string;
  comments_count: number;
  card_type?: string;
  type: string;
  parsed_at: string;
}