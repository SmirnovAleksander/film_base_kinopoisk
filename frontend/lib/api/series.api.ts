import { apiClient } from './client.api';
import type {
    Series,
    SeriesReadWithDetails,
    SeriesSearchResponse,
    ContentWatchProvider,
    SimilarContent,
    ContentStills,
} from '@/lib/types';
import type { Stuff } from '@/lib/types';
import { API_ENDPOINTS, PAGINATION } from '@/lib/config';
import { buildQueryString } from './client.api';

export class SeriesAPI {
    // Получить список сериалов
    static async getSeries(
        page: number = 1,
        pageSize: number = PAGINATION.DEFAULT_PAGE_SIZE
    ): Promise<SeriesSearchResponse> {
        const params = {
            page,
            page_size: pageSize,
        };
        const response = await apiClient.get(`${API_ENDPOINTS.SERIES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    // Поиск сериалов
    static async searchSeries(query: string, page: number = 1): Promise<SeriesSearchResponse> {
        const queryParams = {
            query,
            page,
            page_size: PAGINATION.DEFAULT_PAGE_SIZE,
        };
        const response = await apiClient.get(`${API_ENDPOINTS.SERIES.SEARCH}${buildQueryString(queryParams)}`);
        return response.data;
    }

    // Получить детали сериала
    static async getSeriesDetails(id: number): Promise<SeriesReadWithDetails> {
        const response = await apiClient.get(API_ENDPOINTS.SERIES.DETAILS(id));
        return response.data;
    }

    // Получить участников сериала
    static async getSeriesStuff(
        id: number,
        role: string = 'all'
    ): Promise<Stuff[]> {
        const params = {
            role,
        };
        const response = await apiClient.get(`${API_ENDPOINTS.SERIES.STUFF(id)}${buildQueryString(params)}`);
        return response.data;
    }

    // Получить кадры сериала
    static async getSeriesStills(id: number): Promise<ContentStills> {
        const response = await apiClient.get(API_ENDPOINTS.SERIES.STILL(id));
        return response.data;
    }

    // Получить провайдеры для просмотра сериала
    static async getSeriesWatchProviders(id: number): Promise<ContentWatchProvider[]> {
        const response = await apiClient.get(API_ENDPOINTS.SERIES.WATCH_PROVIDERS(id));
        return response.data;
    }

    // Получить похожий контент
    static async getSimilarSeries(id: number): Promise<SimilarContent[]> {
        const response = await apiClient.get(API_ENDPOINTS.SERIES.SIMILAR(id));
        return response.data;
    }
}
