// Типы для авторизации и пользователей

// Ответ сервера с токеном
export interface BearerResponse {
  access_token: string;
  token_type: string;
}

// Данные для входа в систему
export interface LoginData {
  email: string;
  password: string;
}

// Данные для регистрации
export interface RegisterData {
  email: string;
  password: string;
}

// Схема пользователя
export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
  username: string;
  first_name?: string;
  last_name?: string;
}

// Схема для создания пользователя
export interface UserCreate {
  email: string;
  password: string;
  is_active?: boolean;
  is_superuser?: boolean;
  is_verified?: boolean;
  username: string;
  first_name?: string;
  last_name?: string;
}

// Схема для обновления пользователя
export interface UserUpdate {
  password?: string;
  email?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  is_verified?: boolean;
  username?: string;
  first_name?: string;
  last_name?: string;
}

// Данные для сброса пароля
export interface ResetPasswordData {
  token: string;
  password: string;
}

// Данные для запроса восстановления пароля
export interface ForgotPasswordData {
  email: string;
}

// Данные для запроса верификации email
export interface VerifyRequestData {
  email: string;
}

// Данные для подтверждения email
export interface VerifyData {
  token: string;
}

// Схема тела запроса для OAuth2 login
export interface OAuthLoginBody {
  grant_type: string | null;
  username: string;
  password: string;
  scope: string;
  client_id: string | null;
  client_secret: string | null;
}

// Схема тела запроса для сброса пароля
export interface ResetPasswordBody {
  token: string;
  password: string;
}

// Схема тела запроса для восстановления пароля
export interface ForgotPasswordBody {
  email: string;
}

// Схема тела запроса для запроса верификации
export interface VerifyRequestTokenBody {
  email: string;
}

// Схема тела запроса для подтверждения
export interface VerifyBody {
  token: string;
}