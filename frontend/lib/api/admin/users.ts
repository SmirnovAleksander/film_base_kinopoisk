import { apiClient, buildQueryString } from '../client.api';
import { User } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminUsersAPI {
    // Создать пользователя
    static async createUser(userData: any): Promise<User> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.USERS.CREATE, userData);
        return response.data;
    }

    // Получить список всех пользователей
    static async getAllUsers(
        page: number = 1,
        pageSize: number = 50
    ): Promise<User[]> {
        const params = {
            page,
            page_size: pageSize,
        };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.USERS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    // Получить пользователя по ID
    static async getUserById(id: number): Promise<User> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.USERS.DETAILS(id));
        return response.data;
    }

    // Обновить пользователя
    static async updateUser(id: number, userData: any): Promise<User> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.USERS.UPDATE(id), userData);
        return response.data;
    }

    // Удалить пользователя
    static async deleteUser(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.USERS.DELETE(id));
        return response.data;
    }
}
