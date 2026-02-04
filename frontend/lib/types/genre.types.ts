// Типы для жанров

interface BaseGenre {
    name: string;
}

export type GenreCreate = BaseGenre;
export type GenreUpdate = BaseGenre;

export interface Genre extends BaseGenre {
    id: number;
}
