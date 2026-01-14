import { apiClient, buildQueryString } from '../client.api';
import {
    SimilarFilmRead,
    SimilarFilmCreate,
    SimilarFilmUpdate,
    FilmStill,
    FilmStillCreate,
    FilmStillUpdate,
    FilmWatchProviderRead,
    FilmWatchProviderCreate,
    FilmWatchProviderUpdate,
} from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminFilmDetailsAPI {
    // похожие фильмы

    static async createSimilarFilm(data: SimilarFilmCreate): Promise<SimilarFilmRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.CREATE, data);
        return response.data;
    }

    static async getAllSimilarFilms(page: number = 1, pageSize: number = 50): Promise<SimilarFilmRead[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.SIMILAR_FILMS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getSimilarFilmById(id: number): Promise<SimilarFilmRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.DETAILS(id));
        return response.data;
    }

    static async updateSimilarFilm(id: number, data: SimilarFilmUpdate): Promise<SimilarFilmRead> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.UPDATE(id), data);
        return response.data;
    }

    static async deleteSimilarFilm(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.SIMILAR_FILMS.DELETE(id));
        return response.data;
    }

    // кадры фильма

    static async createFilmStill(data: FilmStillCreate): Promise<FilmStill> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_STILLS.CREATE, data);
        return response.data;
    }

    static async getAllFilmStills(page: number = 1, pageSize: number = 50): Promise<FilmStill[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_STILLS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getFilmStillById(id: number): Promise<FilmStill> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_STILLS.DETAILS(id));
        return response.data;
    }

    static async updateFilmStill(id: number, data: FilmStillUpdate): Promise<FilmStill> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILM_STILLS.UPDATE(id), data);
        return response.data;
    }

    static async deleteFilmStill(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_STILLS.DELETE(id));
        return response.data;
    }

    // провайдеры просмотра

    static async createFilmWatchProvider(data: FilmWatchProviderCreate): Promise<FilmWatchProviderRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.CREATE, data);
        return response.data;
    }

    static async getAllFilmWatchProviders(page: number = 1, pageSize: number = 50): Promise<FilmWatchProviderRead[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getFilmWatchProviderById(id: number): Promise<FilmWatchProviderRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.DETAILS(id));
        return response.data;
    }

    static async updateFilmWatchProvider(id: number, data: FilmWatchProviderUpdate): Promise<FilmWatchProviderRead> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.UPDATE(id), data);
        return response.data;
    }

    static async deleteFilmWatchProvider(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILM_WATCH_PROVIDERS.DELETE(id));
        return response.data;
    }
}
