// Типы для участников (актеров, режиссеров и другого персонала)

// Участник фильма (актер, режиссер и т.д.)
export interface Stuff {
  kinopoisk_id: string;
  name?: string;
  original_name?: string;
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

// Схема для создания участника
export interface StuffCreate {
  kinopoisk_id: string;
  name?: string;
  original_name?: string;
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

// Схема для обновления участника
export interface StuffUpdate {
  name?: string;
  original_name?: string;
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

// Ответ для списка участников
export interface StuffListResponse {
  items: Stuff[];
  page: number;
  page_size: number;
  total_count: number;
}