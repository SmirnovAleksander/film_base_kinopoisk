import { apiClient, buildQueryString } from '../client.api';
import {
    FilmGenreRead,
    FilmGenreCreate,
    FilmCountryRead,
    FilmCountryCreate,
    FilmStuffRead,
    FilmStuffCreate,
    FilmStuffUpdate,
} from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminFilmRelationsAPI {
    // жанры фильма

    static async createFilmGenre(data: FilmGenreCreate): Promise<FilmGenreRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_GENRES.CREATE, data);
        return response.data;
    }

    static async getAllFilmGenres(page: number = 1, pageSize: number = 50): Promise<FilmGenreRead[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_GENRES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getFilmGenreById(id: number): Promise<FilmGenreRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_GENRES.DETAILS(id));
        return response.data;
    }

    static async deleteFilmGenre(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_GENRES.DELETE(id));
        return response.data;
    }

    // страны фильма

    static async createFilmCountry(data: FilmCountryCreate): Promise<FilmCountryRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_COUNTRIES.CREATE, data);
        return response.data;
    }

    static async getAllFilmCountries(page: number = 1, pageSize: number = 50): Promise<FilmCountryRead[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_COUNTRIES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getFilmCountryById(id: number): Promise<FilmCountryRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_COUNTRIES.DETAILS(id));
        return response.data;
    }

    static async deleteFilmCountry(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_COUNTRIES.DELETE(id));
        return response.data;
    }

    // участники фильма

    static async createFilmStuff(data: FilmStuffCreate): Promise<FilmStuffRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_STUFF.CREATE, data);
        return response.data;
    }

    static async getAllFilmStuff(page: number = 1, pageSize: number = 50): Promise<FilmStuffRead[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_STUFF.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getFilmStuffById(id: number): Promise<FilmStuffRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_STUFF.DETAILS(id));
        return response.data;
    }

    static async updateFilmStuff(id: number, data: FilmStuffUpdate): Promise<FilmStuffRead> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILM_STUFF.UPDATE(id), data);
        return response.data;
    }

    static async deleteFilmStuff(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_STUFF.DELETE(id));
        return response.data;
    }
}
