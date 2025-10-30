// Общие типы для ошибок, пагинации и ответов

// ========== БАЗОВЫЕ ОТВЕТЫ ==========

// Базовый ответ для операций (создание, обновление, удаление)
export interface OperationResponse {
  status: string;
  message?: string | null;
  id?: number | null;
}

// Ошибка валидации
export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

// Ошибка HTTP валидации
export interface HTTPValidationError {
  detail: ValidationError[];
}

// Ошибка модели
export interface ErrorModel {
  detail: string | object;
}

// ========== ПАГИНАЦИЯ ==========

// Общий ответ с пагинацией
export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total_count: number;
}

// ========== СПИСКИ И КОЛЛЕКЦИИ ==========

// Ответ для списка участников
export interface StuffListResponse {
  items: any[];
  page: number;
  page_size: number;
  total_count: number;
}