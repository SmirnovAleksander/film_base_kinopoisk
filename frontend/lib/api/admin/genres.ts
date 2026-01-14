import { apiClient } from '../client.api';
import { Genre } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminGenresAPI {
    // Создать жанр
    static async createGenre(genreData: { name: string }): Promise<Genre> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.GENRES.CREATE, genreData);
        return response.data;
    }

    // Получить список всех жанров
    static async getAllGenres(): Promise<Genre[]> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.GENRES.LIST);
        return response.data;
    }

    // Получить жанр по ID
    static async getGenreById(id: number): Promise<Genre> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.GENRES.DETAILS(id));
        return response.data;
    }

    // Обновить жанр
    static async updateGenre(id: number, genreData: { name: string }): Promise<Genre> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.GENRES.UPDATE(id), genreData);
        return response.data;
    }

    // Удалить жанр
    static async deleteGenre(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.GENRES.DELETE(id));
        return response.data;
    }
}
