export interface ContentImage {
    id: number;
    content_id: number;
    content_type: string;
    picture_id: string;
    image_url: string;
    image_type: string;
}

export interface ContentImageCreate {
    content_id: number;
    content_type: string;
    picture_id: string;
    image_url: string;
    image_type: string;
}

export interface ContentWatchProvider {
    id: number;
    content_id: number;
    content_type: string;
    provider_name: string;
    provider_url: string;
    provider_logo?: string | null;
}

export interface ContentWatchProviderCreate {
    content_id: number;
    content_type: string;
    provider_name: string;
    provider_url: string;
    provider_logo?: string | null;
}

export interface SimilarContent {
    id: number;
    content_id: number;
    content_type: string;
    similar_id: string;
    similar_type: string;
    title_ru?: string | null;
    release_year?: number | null;
    genres?: string[] | null;
    poster_url?: string | null;
    rating_kp?: number | null;
}

export interface SimilarContentCreate {
    content_id: number;
    content_type: string;
    similar_id: string;
    similar_type: string;
    title_ru?: string | null;
    release_year?: number | null;
    genres?: string[] | null;
    poster_url?: string | null;
    rating_kp?: number | null;
}

export interface ContentGenreRead {
    id: number;
    content_id: number;
    content_type: string;
    genre_id: number;
}

export interface ContentGenreCreate {
    content_id: number;
    content_type: string;
    genre_id: number;
}

export interface ContentCountryRead {
    id: number;
    content_id: number;
    content_type: string;
    country_id: number;
}

export interface ContentCountryCreate {
    content_id: number;
    content_type: string;
    country_id: number;
}

export interface ContentStuffRead {
    id: number;
    content_id: number;
    content_type: string;
    stuff_id: number;
    role?: string | null;
}

export interface ContentStuffCreate {
    content_id: number;
    content_type: string;
    stuff_id: number;
    role?: string | null;
}

// Полезные типы для фронтенда (группировка)
export interface Still {
    id: string;
    original: string;
}

export interface ContentStills {
    stills?: Still[];
    wall?: Still[];
    shooting?: Still[];
    screenshots?: Still[];
}
