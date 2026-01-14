// Типы для дополнительных деталей фильма (кадры, провайдеры, похожие фильмы)

// Кадры (Stills)
export interface Still {
    id: string;
    original: string;
}

export type FilmStillType = 'stills' | 'wall' | 'shooting' | 'screenshots';

export interface FilmStills {
    stills?: Still[];
    wall?: Still[];
    shooting?: Still[];
    screenshots?: Still[];
}

interface BaseFilmStill {
    picture_id?: string | null;
    original_url?: string | null;
    source?: string | null;
}

export interface FilmStillUpdate extends BaseFilmStill { }

export interface FilmStillCreate extends BaseFilmStill {
    film_id: number;
    picture_id: string;
    original_url: string;
    source: string;
}

export interface FilmStill extends FilmStillCreate {
    id: number;
    source: FilmStillType;
}

// Провайдеры (Watch Providers)
export interface FilmWatchProvider {
    id: number;
    name: string;
    url: string;
    logo?: string | null;
}

interface BaseFilmWatchProvider {
    name?: string | null;
    url?: string | null;
    logo?: string | null;
}

export interface FilmWatchProviderUpdate extends BaseFilmWatchProvider {
    film_id?: number | null;
}

export interface FilmWatchProviderCreate extends BaseFilmWatchProvider {
    film_id: number;
    name: string;
    url: string;
}

export interface FilmWatchProviderRead extends FilmWatchProviderCreate {
    id: number;
}

// Похожие фильмы (Similar Films)
export interface SimilarFilm {
    id: number;
    similar_film_id: string;
    similar_film_title: string;
    similar_film_year?: string | null;
    similar_film_genres?: string[] | null;
    similar_film_poster?: string | null;
    similar_film_rating?: string | null;
}

interface BaseSimilarFilm {
    similar_film_title?: string | null;
    similar_film_year?: string | null;
    similar_film_genres?: string[] | null;
    similar_film_poster?: string | null;
    similar_film_rating?: string | null;
}

export interface SimilarFilmUpdate extends BaseSimilarFilm { }

export interface SimilarFilmCreate extends BaseSimilarFilm {
    film_id: number;
    similar_film_id: string;
    similar_film_title: string;
}

export interface SimilarFilmRead extends SimilarFilmCreate {
    id: number;
}
