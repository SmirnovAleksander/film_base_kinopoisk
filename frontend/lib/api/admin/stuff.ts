import { apiClient, buildQueryString } from '../client.api';
import { Stuff } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminStuffAPI {
    // Создать участника
    static async createStuff(stuffData: any): Promise<Stuff> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.STUFF.CREATE, stuffData);
        return response.data;
    }

    // Получить список всех участников
    static async getAllStuff(
        page: number = 1,
        pageSize: number = 50
    ): Promise<any> {
        const params = {
            page,
            page_size: Math.min(pageSize, 100),
        };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.STUFF.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    // Получить все участники
    static async getAllStuffAll(): Promise<Stuff[]> {
        const allStuff: Stuff[] = [];
        let page = 1;
        let hasMore = true;

        while (hasMore) {
            const response = await this.getAllStuff(page, 100);
            if (response && Array.isArray(response.items)) {
                allStuff.push(...response.items);
                const totalCount = response.total_count || 0;
                hasMore = response.items.length === 100 && totalCount > page * 100;
            } else if (Array.isArray(response)) {
                allStuff.push(...response);
                hasMore = response.length === 100;
            } else {
                hasMore = false;
            }
            page++;
            if (page > 1000) break;
        }

        return allStuff;
    }

    // Получить участника по ID
    static async getStuffById(id: number): Promise<Stuff> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.STUFF.DETAILS(id));
        return response.data;
    }

    // Обновить участника
    static async updateStuff(id: number, stuffData: any): Promise<Stuff> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.STUFF.UPDATE(id), stuffData);
        return response.data;
    }

    // Удалить участника
    static async deleteStuff(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.STUFF.DELETE(id));
        return response.data;
    }
}
