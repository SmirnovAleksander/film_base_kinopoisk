import { Genre } from './genres.types';
import { Country } from './countries.types';
import { Stuff } from './stuff.types';
import {
  ContentImage,
  ContentWatchProvider,
  SimilarContent
} from './content-details.types';
import type { PaginatedResponse } from './common.types';

// Типы для фильмов
export interface Film {
  id: number;
  kinopoisk_id: string;
  title_ru?: string | null;
  title_en?: string | null;
  description_short?: string | null;
  description_full?: string | null;
  poster_url?: string | null;
  release_year?: number | null;
  tagline?: string | null;
  premiere_ru?: string | null;
  premiere_world?: string | null;
  content_type: string;
  is_family: boolean;
  duration?: string | null;

  rating_kp?: number | null;
  votes_kp?: number | null;
  rating_imdb?: number | null;
  votes_imdb?: number | null;
  rating_user?: number | null;
  votes_user: number;

  budget?: string | null;
  box_office_usa?: string | null;
  box_office_rus?: string | null;
}

export interface FilmReadWithDetails extends Film {
  genres: Genre[];
  countries: Country[];
  stuff: Stuff[];
  images: ContentImage[];
  watch_providers: ContentWatchProvider[];
  similar_content: SimilarContent[];
}

export interface FilmCreate {
  kinopoisk_id: string;
  title_ru?: string | null;
  title_en?: string | null;
  description_short?: string | null;
  description_full?: string | null;
  poster_url?: string | null;
  release_year?: number | null;
  tagline?: string | null;
  premiere_ru?: string | null;
  premiere_world?: string | null;
  is_family?: boolean | null;
  duration?: string | null;
  rating_kp?: number | null;
  votes_kp?: number | null;
  rating_imdb?: number | null;
  votes_imdb?: number | null;
}

export interface FilmUpdate {
  title_ru?: string | null;
  title_en?: string | null;
  description_short?: string | null;
  description_full?: string | null;
  poster_url?: string | null;
  release_year?: number | null;
  tagline?: string | null;
  premiere_ru?: string | null;
  premiere_world?: string | null;
  is_family?: boolean | null;
  duration?: string | null;
  rating_kp?: number | null;
  votes_kp?: number | null;
  rating_imdb?: number | null;
  votes_imdb?: number | null;
}

export interface FilmRecommendation extends Film {
  relevance_score: number;
  genre_matches: number;
  stuff_matches: number;
}

export interface FilmRecommendationsResponse {
  items: FilmRecommendation[];
  total_count: number;
}

export type FilmSearchResponse = PaginatedResponse<Film>;

export interface FilmFilterParams {
  genre_id?: number;
  country_id?: number;
  start_year?: number;
  end_year?: number;
  title?: string;
  lang?: string;
  source?: string;
  min_rating?: number;
  max_rating?: number;
  page?: number;
  page_size?: number;
}

export interface FilmSearchParams {
  query: string;
  lang?: string;
  page?: number;
  page_size?: number;
}