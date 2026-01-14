// Типы для стран

interface BaseCountry {
    name: string;
}

export interface CountryCreate extends BaseCountry { }
export interface CountryUpdate extends BaseCountry { }

export interface Country extends BaseCountry {
    id: number;
}
