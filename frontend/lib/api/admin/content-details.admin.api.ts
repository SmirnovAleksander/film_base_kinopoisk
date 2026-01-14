import { apiClient, buildQueryString } from '../client.api';
import {
    ContentImage,
    ContentWatchProvider,
    SimilarContent,
    ContentGenreRead,
    ContentCountryRead,
    ContentStuffRead,
} from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminContentDetailsAPI {
    // Изображения
    static async createContentImage(data: any): Promise<ContentImage> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.CONTENT_IMAGES.CREATE, data);
        return response.data;
    }

    static async getAllContentImages(params: { content_id?: number, content_type?: string, image_type?: string }): Promise<ContentImage[]> {
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.CONTENT_IMAGES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getContentImageById(id: number): Promise<ContentImage> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.CONTENT_IMAGES.DETAILS(id));
        return response.data;
    }

    static async deleteContentImage(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.CONTENT_IMAGES.DELETE(id));
        return response.data;
    }

    // Провайдеры
    static async createContentWatchProvider(data: any): Promise<ContentWatchProvider> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.CONTENT_WATCH_PROVIDERS.CREATE, data);
        return response.data;
    }

    static async getAllContentWatchProviders(params: { content_id?: number, content_type?: string }): Promise<ContentWatchProvider[]> {
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.CONTENT_WATCH_PROVIDERS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getContentWatchProviderById(id: number): Promise<ContentWatchProvider> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.CONTENT_WATCH_PROVIDERS.DETAILS(id));
        return response.data;
    }

    static async deleteContentWatchProvider(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.CONTENT_WATCH_PROVIDERS.DELETE(id));
        return response.data;
    }

    // Похожий контент
    static async createSimilarContent(data: any): Promise<SimilarContent> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.SIMILAR_CONTENT.CREATE, data);
        return response.data;
    }

    static async getAllSimilarContent(params: { content_id?: number, content_type?: string }): Promise<SimilarContent[]> {
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.SIMILAR_CONTENT.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getSimilarContentById(id: number): Promise<SimilarContent> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.SIMILAR_CONTENT.DETAILS(id));
        return response.data;
    }

    static async deleteSimilarContent(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.SIMILAR_CONTENT.DELETE(id));
        return response.data;
    }

    // Связи с жанрами
    static async createContentGenre(data: any): Promise<ContentGenreRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.CONTENT_GENRES.CREATE, data);
        return response.data;
    }

    static async getAllContentGenres(params: { content_id?: number, content_type?: string, genre_id?: number }): Promise<ContentGenreRead[]> {
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.CONTENT_GENRES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getContentGenreById(id: number): Promise<ContentGenreRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.CONTENT_GENRES.DETAILS(id));
        return response.data;
    }

    static async deleteContentGenre(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.CONTENT_GENRES.DELETE(id));
        return response.data;
    }

    // Связи со странами
    static async createContentCountry(data: any): Promise<ContentCountryRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.CONTENT_COUNTRIES.CREATE, data);
        return response.data;
    }

    static async getAllContentCountries(params: { content_id?: number, content_type?: string, country_id?: number }): Promise<ContentCountryRead[]> {
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.CONTENT_COUNTRIES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getContentCountryById(id: number): Promise<ContentCountryRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.CONTENT_COUNTRIES.DETAILS(id));
        return response.data;
    }

    static async deleteContentCountry(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.CONTENT_COUNTRIES.DELETE(id));
        return response.data;
    }

    // Связи с участниками
    static async createContentStuff(data: any): Promise<ContentStuffRead> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.CONTENT_STUFF.CREATE, data);
        return response.data;
    }

    static async getAllContentStuff(params: { content_id?: number, content_type?: string, stuff_id?: number }): Promise<ContentStuffRead[]> {
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.CONTENT_STUFF.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getContentStuffById(id: number): Promise<ContentStuffRead> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.CONTENT_STUFF.DETAILS(id));
        return response.data;
    }

    static async deleteContentStuff(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.CONTENT_STUFF.DELETE(id));
        return response.data;
    }
}
