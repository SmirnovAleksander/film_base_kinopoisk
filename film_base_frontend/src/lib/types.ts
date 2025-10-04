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

export type UserMe = {
  id: number;
  email: string;
  username: string | null;
  is_email_verified: boolean;
  role: string;
  created_at: string | null;
  last_login_at: string | null;
};


