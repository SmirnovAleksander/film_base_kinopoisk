import { Genre } from './genres.types';
import { Country } from './countries.types';
import { Stuff } from './stuff.types';
import {
    ContentImage,
    ContentWatchProvider,
    SimilarContent
} from './content-details.types';
import type { PaginatedResponse } from './common.types';

export type SeriesSearchResponse = PaginatedResponse<Series>;

export interface Series {
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

    rating_kp?: number | null;
    votes_kp?: number | null;
    rating_imdb?: number | null;
    votes_imdb?: number | null;
    rating_user?: number | null;
    votes_user: number;

    platform?: string | null;
    episodes_count?: number | null;
}

export interface SeriesReadWithDetails extends Series {
    genres: Genre[];
    countries: Country[];
    stuff: Stuff[];
    images: ContentImage[];
    watch_providers: ContentWatchProvider[];
    similar_content: SimilarContent[];
}

export interface SeriesUpdate {
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
    rating_kp?: number | null;
    votes_kp?: number | null;
    rating_imdb?: number | null;
    votes_imdb?: number | null;
    rating_user?: number | null;
    votes_user?: number | null;
    platform?: string | null;
    episodes_count?: number | null;
}
