import { apiClient, buildQueryString } from '../client.api';
import { Series } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminSeriesAPI {
    static async createSeries(seriesData: any): Promise<Series> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.SERIES.CREATE, seriesData);
        return response.data;
    }

    static async getAllSeries(page: number = 1, pageSize: number = 50): Promise<Series[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.SERIES.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getSeriesById(id: number): Promise<Series> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.SERIES.DETAILS(id));
        return response.data;
    }

    static async updateSeries(id: number, seriesData: any): Promise<Series> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.SERIES.UPDATE(id), seriesData);
        return response.data;
    }

    static async deleteSeries(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.SERIES.DELETE(id));
        return response.data;
    }
}
