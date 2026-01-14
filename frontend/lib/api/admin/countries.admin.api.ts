import { apiClient } from '../client.api';
import { Country } from '@/lib/types';
import { API_ENDPOINTS } from '@/lib/config';

export class AdminCountriesAPI {
    static async createCountry(countryData: { name: string }): Promise<Country> {
        const response = await apiClient.post(API_ENDPOINTS.ADMIN.COUNTRIES.CREATE, countryData);
        return response.data;
    }

    static async getAllCountries(): Promise<Country[]> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.COUNTRIES.LIST);
        return response.data;
    }

    static async getCountryById(id: number): Promise<Country> {
        const response = await apiClient.get(API_ENDPOINTS.ADMIN.COUNTRIES.DETAILS(id));
        return response.data;
    }

    static async updateCountry(id: number, countryData: { name: string }): Promise<Country> {
        const response = await apiClient.put(API_ENDPOINTS.ADMIN.COUNTRIES.UPDATE(id), countryData);
        return response.data;
    }

    static async deleteCountry(id: number): Promise<any> {
        const response = await apiClient.delete(API_ENDPOINTS.ADMIN.COUNTRIES.DELETE(id));
        return response.data;
    }
}
