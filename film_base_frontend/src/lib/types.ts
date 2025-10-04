export type FilmListItem = {
  id: number;
  kinopoisk_id: number | null;
  title: string;
  original_title?: string | null;
  full_description?: string | null;
  poster: string | null;
  year?: number | null;
  duration?: number | string | null;
  rating_kp: number | null;
  rating_imdb?: number | null;
};

export type Paginated<T> = {
  items: T[];
  page: number;
  page_size: number;
};

export type FilmDetails = {
  id: number;
  kinopoisk_id: number | null;
  title: string;
  original_title: string | null;
  description: string | null;
  full_description: string | null;
  poster: string | null;
  year: number | null;
  tagline?: string | null;
  ru_premiere?: string | null;
  world_premiere?: string | null;
  age_rating?: string | number | null;
  duration: number | string | null;
  rating_kp: number | null;
  kp_votes_count: number | null;
  rating_imdb: number | null;
  imdb_votes_count: number | null;
  budget?: string | null;
  usa_box_office?: string | null;
  rus_box_office?: string | null;
  mpaa_rating?: string | null;
  user_rating?: number | null;
  user_rating_count?: number | null;
};

export type WatchProvider = { name: string; url: string; logo: string | null };
export type SimilarFilm = { kinopoisk_id: number; title: string };

export type UserRating = {
  rating: number;
  created_at: string;
  updated_at: string;
};

export type FilmAverageRating = {
  average_rating: number | null;
  total_ratings: number;
  min_rating: number | null;
  max_rating: number | null;
};

export type UserRatingWithFilm = {
  rating: number;
  created_at: string;
  updated_at: string;
  film: {
    id: number;
    title: string;
    poster: string | null;
    year: number | null;
  };
};

export type Actor = {
  id: number;
  kinopoisk_id: string;
  name: string;
  english_name: string | null;
  career: string[] | null;
  ganres: string[] | null;
  height: string | null;
  birthday_day_month: string | null;
  birthday_year: number | null;
  zodiac: string | null;
  age: number | null;
  birthplace: string[] | null;
  spouse: string[] | null;
  children: string[] | null;
  total_films: number | null;
  career_start_year: number | null;
  career_end_year: number | null;
  photo: string | null;
};

export type UserRole = "user" | "moderator" | "admin";

export type UserMe = {
  id: number;
  email: string;
  username: string | null;
  is_email_verified: boolean;
  role: UserRole;
  created_at: string | null;
  last_login_at: string | null;
};

export type User = {
  id: number;
  email: string;
  username: string | null;
  is_email_verified: boolean;
  role: UserRole;
  created_at: string | null;
  last_login_at: string | null;
};

export type UserStats = {
  total_users: number;
  verified_users: number;
  unverified_users: number;
  role_distribution: Record<UserRole, number>;
  new_users_30d: number;
};

export type CommentModeration = {
  id: number;
  film_id: number;
  user_id: number;
  content: string;
  created_at: string;
  film_title: string;
  user_email: string;
  username: string | null;
};

export type ModerationStats = {
  total_comments: number;
  status_distribution: Record<string, number>;
  comments_7d: number;
  pending_comments: number;
};


