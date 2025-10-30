// Типы для участников/актеров

export interface Stuff {
  kinopoisk_id: string;
  name?: string | null;
  original_name?: string | null;
  career?: string[] | null;
  ganres?: string[] | null;
  height?: string | null;
  birthday_day_month?: string | null;
  zodiac?: string | null;
  age?: number | null;
  birthplace?: string[] | null;
  spouse?: string[] | null;
  children?: string[] | null;
  total_films?: number | null;
  career_start_year?: number | null;
  career_end_year?: number | null;
  image?: string | null;
  id: number;
}

export interface StuffCreate {
  kinopoisk_id: string;
  name?: string | null;
  original_name?: string | null;
  career?: string[] | null;
  ganres?: string[] | null;
  height?: string | null;
  birthday_day_month?: string | null;
  zodiac?: string | null;
  age?: number | null;
  birthplace?: string[] | null;
  spouse?: string[] | null;
  children?: string[] | null;
  total_films?: number | null;
  career_start_year?: number | null;
  career_end_year?: number | null;
  image?: string | null;
}

export interface StuffUpdate {
  name?: string | null;
  original_name?: string | null;
  career?: string[] | null;
  ganres?: string[] | null;
  height?: string | null;
  birthday_day_month?: string | null;
  zodiac?: string | null;
  age?: number | null;
  birthplace?: string[] | null;
  spouse?: string[] | null;
  children?: string[] | null;
  total_films?: number | null;
  career_start_year?: number | null;
  career_end_year?: number | null;
  image?: string | null;
}

export interface StuffListResponse {
  items: Stuff[];
  page: number;
  page_size: number;
  total_count: number;
}

// Алиас для совместимости с API
export type StuffResponse = StuffListResponse;