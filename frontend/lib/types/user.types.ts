/**
 * Типы для пользователей
 */

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  is_superuser: boolean;
}