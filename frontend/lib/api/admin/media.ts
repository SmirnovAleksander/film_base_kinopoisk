import { apiClient, buildQueryString } from '../client.api';
import { Media } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminMediaAPI {
    // Создать медиа
    static async createMedia(mediaData: any): Promise<Media> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.MEDIA.CREATE, mediaData);
        return response.data;
    }

    // Получить список всех медиа
    static async getAllMedia(
        page: number = 1,
        pageSize: number = 50
    ): Promise<Media[]> {
        const params = {
            page,
            page_size: pageSize,
        };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.MEDIA.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    // Получить медиа по ID
    static async getMediaById(id: number): Promise<Media> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.MEDIA.DETAILS(id));
        return response.data;
    }

    // Обновить медиа
    static async updateMedia(id: number, mediaData: any): Promise<Media> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.MEDIA.UPDATE(id), mediaData);
        return response.data;
    }

    // Удалить медиа
    static async deleteMedia(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.MEDIA.DELETE(id));
        return response.data;
    }
}
