// Типы для участников/актеров

interface BaseStuff {
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

export type StuffUpdate = BaseStuff;

export interface StuffCreate extends BaseStuff {
  kinopoisk_id: string;
}

export interface Stuff extends StuffCreate {
  id: number;
}

export interface StuffResponse {
  items: Stuff[];
  page: number;
  page_size: number;
  total_count: number;
}