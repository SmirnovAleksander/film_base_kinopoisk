import { apiClient, buildQueryString } from '../client.api';
import { Stuff, StuffResponse } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminStuffAPI {
    static async createStuff(stuffData: any): Promise<Stuff> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.STUFF.CREATE, stuffData);
        return response.data;
    }

    static async getAllStuff(page: number = 1, pageSize: number = 50): Promise<StuffResponse> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.STUFF.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getStuffById(id: number): Promise<Stuff> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.STUFF.DETAILS(id));
        return response.data;
    }

    static async updateStuff(id: number, stuffData: any): Promise<Stuff> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.STUFF.UPDATE(id), stuffData);
        return response.data;
    }

    static async deleteStuff(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.STUFF.DELETE(id));
        return response.data;
    }
}
