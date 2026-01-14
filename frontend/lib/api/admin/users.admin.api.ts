import { apiClient, buildQueryString } from '../client.api';
import { User, UserCreate, UserUpdate } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminUsersAPI {
    static async createUser(userData: UserCreate): Promise<User> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.USERS.CREATE, userData);
        return response.data;
    }

    static async getAllUsers(page: number = 1, pageSize: number = 50): Promise<User[]> {
        const params = { page, page_size: pageSize };
        const response = await apiClient.get(`${API_ENDPOINTS.ADMIN.USERS.LIST}${buildQueryString(params)}`);
        return response.data;
    }

    static async getUserById(id: number): Promise<User> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.USERS.DETAILS(id));
        return response.data;
    }

    static async updateUser(id: number, userData: UserUpdate): Promise<User> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.USERS.UPDATE(id), userData);
        return response.data;
    }

    static async deleteUser(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.USERS.DELETE(id));
        return response.data;
    }
}
