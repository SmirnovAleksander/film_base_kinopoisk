// Типы для связей фильма с другими сущностями (жанры, страны, персонал)

export interface FilmGenreCreate {
    film_id: number;
    genre_id: number;
}

export interface FilmGenreRead extends FilmGenreCreate {
    id: number;
}

export interface FilmCountryCreate {
    film_id: number;
    country_id: number;
}

export interface FilmCountryRead extends FilmCountryCreate {
    id: number;
}

interface BaseFilmStuff {
    role?: string | null;
}

export interface FilmStuffUpdate extends BaseFilmStuff { }

export interface FilmStuffCreate extends BaseFilmStuff {
    film_id: number;
    stuff_id: number;
}

export interface FilmStuffRead extends FilmStuffCreate {
    id: number;
}
