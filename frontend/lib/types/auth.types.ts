// Типы для аутентификации

export interface BearerResponse {
  access_token: string;
  token_type: string;
}

export interface BodyAuthLogin {
  grant_type?: string;
  username: string;
  password: string;
  scope?: string;
  client_id?: string | null;
  client_secret?: string | null;
}

export interface BodyResetForgotPassword {
  email: string;
}

export interface BodyResetResetPassword {
  token: string;
  password: string;
}

export interface BodyVerifyRequestToken {
  email: string;
}

export interface BodyVerifyVerify {
  token: string;
}

export interface UserCreate {
  email: string;
  password: string;
  is_active?: boolean;
  is_superuser?: boolean;
  is_verified?: boolean;
  username: string;
  first_name?: string | null;
  last_name?: string | null;
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
  username: string;
  first_name?: string | null;
  last_name?: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserUpdate {
  password?: string | null;
  email?: string | null;
  is_active?: boolean | null;
  is_superuser?: boolean | null;
  is_verified?: boolean | null;
  username?: string | null;
  first_name?: string | null;
  last_name?: string | null;
}

// Типы для форм входа и регистрации
export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  username: string;
  first_name?: string;
  last_name?: string;
}