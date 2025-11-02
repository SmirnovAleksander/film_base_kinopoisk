'use client';

import { useState, useRef } from 'react';
import { Star } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useUserInteractionsStore } from '@/store';

interface StarRatingProps {
  filmId: number;
  initialRating?: number;
  size?: 'sm' | 'md' | 'lg';
  interactive?: boolean;
  onRatingChange?: (rating: number) => void;
  className?: string;
}

export function StarRating({
  filmId,
  initialRating = 0,
  size = 'md',
  interactive = true,
  onRatingChange,
  className
}: StarRatingProps) {
  const [hoverRating, setHoverRating] = useState(0);
  const [currentRating, setCurrentRating] = useState(initialRating);
  const containerRef = useRef<HTMLDivElement>(null);
  const { setFilmRating, getUserRating, isAddingRating } = useUserInteractionsStore();

  const userRating = currentRating || getUserRating(filmId) || 0;

  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  const handleStarClick = async (rating: number) => {
    if (!interactive || isAddingRating) return;

    setCurrentRating(rating);
    await setFilmRating(filmId, rating);
    onRatingChange?.(rating);
  };

  const handleStarHover = (rating: number) => {
    if (interactive) {
      setHoverRating(rating);
    }
  };

  const handleContainerLeave = () => {
    if (interactive) {
      setHoverRating(0);
    }
  };

  const handleContainerEnter = () => {
    if (interactive) {
      // Восстанавливаем последнее значение hover если оно было
      setHoverRating(userRating > 0 ? 0 : 0);
    }
  };

  const displayRating = hoverRating || userRating;

  return (
    <div
      ref={containerRef}
      className={`flex items-center gap-1 ${className}`}
      onMouseEnter={handleContainerEnter}
      onMouseLeave={handleContainerLeave}
    >
      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((rating) => {
        const isFilled = displayRating >= rating;
        const isHalfFilled = displayRating >= rating - 0.5 && displayRating < rating;
        
        return (
          <Button
            key={rating}
            variant="ghost"
            className={`p-2 rounded-full h-auto w-auto ${
              interactive ? 'cursor-pointer hover:bg-yellow-500/10' : 'cursor-default'
            } transition-colors duration-200`}
            onClick={() => handleStarClick(rating)}
            onMouseEnter={() => handleStarHover(rating)}
            disabled={!interactive || isAddingRating}
          >
            <div className="relative flex items-center justify-center transition-colors duration-200">
              {/* Звезда-фон (серая) */}
              <Star
                className={`${sizeClasses[size]} text-muted-foreground`}
                fill="none"
              />
              
              {/* Звезда-оценка (желтая) */}
              {(isFilled || (isHalfFilled && displayRating >= rating - 0.5)) && (
                <Star
                  className={`absolute top-0 left-0 ${sizeClasses[size]} text-yellow-500 transition-colors duration-200`}
                  fill="currentColor"
                />
              )}
            </div>
          </Button>
        );
      })}
      
      {userRating > 0 && (
        <span className="text-sm text-muted-foreground ml-2">
          {userRating.toFixed(1)}
        </span>
      )}
    </div>
  );
}

// Компонент для отображения среднего рейтинга
interface AverageRatingProps {
  rating?: number;
  totalRatings?: number;
  size?: 'sm' | 'md' | 'lg';
  showCount?: boolean;
  className?: string;
}

export function AverageRating({ 
  rating, 
  totalRatings = 0, 
  size = 'md', 
  showCount = true,
  className 
}: AverageRatingProps) {
  const sizeClasses = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  if (!rating) {
    return (
      <div className={`flex items-center gap-1 text-muted-foreground ${className}`}>
        <Star className={`${sizeClasses[size]} text-muted-foreground`} fill="none" />
        <span className="text-sm">Нет оценок</span>
        {showCount && totalRatings > 0 && (
          <span className="text-xs">({totalRatings})</span>
        )}
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      <Star className={`${sizeClasses[size]} text-yellow-500 fill-current`} />
      <span className="text-sm font-medium">{rating.toFixed(1)}</span>
      {showCount && totalRatings > 0 && (
        <span className="text-xs text-muted-foreground">({totalRatings})</span>
      )}
    </div>
  );
}