'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Star, Heart, Calendar, Eye } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useUserInteractionsStore } from '@/store';
import { useAuth } from '@/hooks/use-auth';
import { ROUTES } from '@/lib/config';
import { formatDuration } from '@/lib/utils';
import { Film } from '@/lib/types';

interface FilmCardProps {
  film: Film;
  showActions?: boolean;
  isExternal?: boolean;
  externalUrl?: string;
  className?: string;
}

export function FilmCard({ film, showActions = true, isExternal = false, externalUrl, className }: FilmCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  
  const { isAuthenticated } = useAuth();
  
  const {
    bookmarkedFilmIds,
    addBookmark,
    removeBookmark,
    ratedFilmIds,
    getUserRating,
    isAddingBookmark
  } = useUserInteractionsStore();

  const isBookmarked = bookmarkedFilmIds.has(film.id);
  const userRating = getUserRating(film.id);
  const isRated = ratedFilmIds.has(film.id);

  const isValidPosterUrl = (url: string): boolean => {
    if (!url || typeof url !== 'string') return false;
    try {
      new URL(url);
      return url.startsWith('http://') || url.startsWith('https://');
    } catch {
      return false;
    }
  };

  const posterUrl = film.poster && isValidPosterUrl(film.poster) ? film.poster : null;

  const handleBookmarkToggle = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (isExternal) return;
    if (!isAuthenticated) return;
    
    if (isBookmarked) {
      await removeBookmark(film.id);
    } else {
      await addBookmark(film.id);
    }
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(true);
  };

  const getRatingColor = (rating: number) => {
    if (rating >= 8) return 'text-green-500';
    if (rating >= 6) return 'text-yellow-500';
    return 'text-red-500';
  };

  const LinkWrapper = isExternal && externalUrl
    ? ({ children }: { children: React.ReactNode }) => (
        <a href={externalUrl} target="_blank" rel="noopener noreferrer" className="block">
          {children}
        </a>
      )
    : ({ children }: { children: React.ReactNode }) => (
        <Link href={ROUTES.FILM_DETAILS(film.id)} className="block">
          {children}
        </Link>
      );

  const cardContent = (
    <>
      {/* Постер фильма */}
      <div className="relative aspect-2/3 overflow-hidden">
        {!imageLoaded && (
          <Skeleton className="absolute inset-0 w-full h-full" />
        )}
        {posterUrl && !imageError ? (
          <Image
            src={posterUrl}
            alt={film.title || 'Без названия'}
            fill
            className={`object-cover transition-transform duration-200 group-hover:scale-105 ${
              !imageLoaded ? 'opacity-0' : 'opacity-100'
            }`}
            onLoad={() => setImageLoaded(true)}
            onError={handleImageError}
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            unoptimized={true}
          />
        ) : (
          <div className="w-full h-full bg-muted flex items-center justify-center">
            <span className="text-muted-foreground">Нет постера</span>
          </div>
        )}
        
        {/* Оверлей с рейтингом */}
        <div className="absolute top-2 right-2 flex flex-col gap-1">
          {film.rating_kp && (
            <Badge variant="secondary" className="bg-background/80 backdrop-blur">
              <Star className="w-3 h-3 mr-1" />
              <span className="text-xs font-medium">{film.rating_kp}</span>
            </Badge>
          )}
        </div>

        {/* Кнопка закладки */}
        {showActions && !isExternal && isAuthenticated && (
          <Button
            size="icon"
            variant={isBookmarked ? "default" : "secondary"}
            className="absolute top-2 left-2 w-8 h-8 opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={handleBookmarkToggle}
            disabled={isAddingBookmark}
          >
            <Heart className={`w-4 h-4 ${isBookmarked ? 'fill-current' : ''}`} />
          </Button>
        )}
      </div>

      <CardContent className="p-4">
        {/* Название */}
        <h3 className="font-semibold text-sm leading-tight mb-2 line-clamp-2 group-hover:text-primary transition-colors">
          {film.title || film.original_title || 'Без названия'}
        </h3>

        {/* Оригинальное название */}
        {film.original_title && film.title !== film.original_title && (
          <p className="text-xs text-muted-foreground mb-2 line-clamp-1">
            {film.original_title}
          </p>
        )}

        {/* Метаинформация */}
        <div className="flex items-center gap-2 text-xs text-muted-foreground mb-3">
          {film.year && (
            <div className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              <span>{film.year}</span>
            </div>
          )}
          {film.duration && (
            <div className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              <span>{formatDuration(film.duration)}</span>
            </div>
          )}
        </div>

        {/* Рейтинги */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {film.rating_kp && (
              <div className="flex items-center gap-1">
                <Badge variant="outline">
                  KP
                  <span className={`text-sm font-medium ${getRatingColor(film.rating_kp)}`}>
                    {film.rating_kp}
                  </span>
                </Badge>
              </div>
            )}
            {film.rating_imdb && (
              <div className="flex items-center gap-1">
                <Badge variant="outline">
                  IMDb
                  <span className={`text-sm font-medium ${getRatingColor(film.rating_imdb)}`}>
                    {film.rating_imdb}
                  </span>
                </Badge>
              </div>
            )}
          </div>

          {/* Пользовательский рейтинг */}
          {isRated && (
            <div className="flex items-center gap-1">
              <Star className="w-3 h-3 text-yellow-500 fill-current" />
              <Badge variant="default" className="text-xs px-1 py-0 bg-yellow-500 text-white">
                {userRating}
              </Badge>
            </div>
          )}
        </div>

        {/* Описание */}
        {(film.description || film.full_description) && (
          <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
            {film.description || film.full_description}
          </p>
        )}
        
        {/* Индикатор внешнего источника */}
        {isExternal && (
          <div className="mt-2">
            <Badge variant="outline" className="text-xs text-blue-600">
              На Kinopoisk
            </Badge>
          </div>
        )}
      </CardContent>
    </>
  );

  return (
    <Card className={`group overflow-hidden transition-all duration-200 pt-0 hover:shadow-lg ${className}`}>
      <LinkWrapper>
        {cardContent}
      </LinkWrapper>
    </Card>
  );
}

export function FilmCardSkeleton({ className }: { className?: string }) {
  return (
    <Card className={className}>
      <div className="aspect-2/3">
        <Skeleton className="w-full h-full" />
      </div>
      <CardContent className="p-4">
        <Skeleton className="h-4 w-3/4 mb-2" />
        <Skeleton className="h-3 w-1/2 mb-2" />
        <Skeleton className="h-3 w-full mb-2" />
        <div className="flex justify-between">
          <Skeleton className="h-3 w-16" />
          <Skeleton className="h-3 w-12" />
        </div>
      </CardContent>
    </Card>
  );
}