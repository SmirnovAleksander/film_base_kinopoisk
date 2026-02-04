// Типы для стран

interface BaseCountry {
    name: string;
}

export type CountryCreate = BaseCountry;
export type CountryUpdate = BaseCountry;

export interface Country extends BaseCountry {
    id: number;
}
