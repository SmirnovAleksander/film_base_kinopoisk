import type { Film } from './film.types';
import type { Series } from './series.types';
import type { PaginatedResponse } from './common.types';

export interface UserContentRating {
    id: number;
    user_id: number;
    content_id: number;
    content_type: string;
    rating: number;
    created_at: string;
    updated_at: string;
    film?: Film | null;
    series?: Series | null;
}

export interface UserContentRatingCreate {
    content_id: number;
    content_type: string;
    rating: number;
}

export interface UserContentRatingUpdate {
    rating: number;
}

export type UserRatingsResponse = PaginatedResponse<UserContentRating>;

export interface ContentAverageRating {
    average_rating?: number | null;
    total_ratings: number;
    min_rating?: number | null;
    max_rating?: number | null;
}

export interface RatingOperationResponse {
    rating?: number | null;
    created_at: string;
    updated_at: string;
}
