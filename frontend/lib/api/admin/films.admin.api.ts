import { apiClient, buildQueryString } from '../client.api';
import { Film } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminFilmsAPI {
    static async createFilm(filmData: any): Promise<Film> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.FILMS.CREATE, filmData);
        return response.data;
    }

    static async getAllFilms(page: number = 1, pageSize: number = 50): Promise<Film[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.FILMS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getFilmById(id: number): Promise<Film> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.FILMS.DETAILS(id));
        return response.data;
    }

    static async updateFilm(id: number, filmData: any): Promise<Film> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.FILMS.UPDATE(id), filmData);
        return response.data;
    }

    static async deleteFilm(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.FILMS.DELETE(id));
        return response.data;
    }
}
