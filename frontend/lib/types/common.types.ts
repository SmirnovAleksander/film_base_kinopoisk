// Общие типы для API

export interface ErrorModel {
  detail: string | Record<string, string>;
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}

export interface OperationResponse {
  status: string;
  message?: string | null;
  id?: number | null;
}