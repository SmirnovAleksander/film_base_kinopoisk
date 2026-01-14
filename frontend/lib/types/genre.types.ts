// Типы для жанров

interface BaseGenre {
    name: string;
}

export interface GenreCreate extends BaseGenre { }
export interface GenreUpdate extends BaseGenre { }

export interface Genre extends BaseGenre {
    id: number;
}
