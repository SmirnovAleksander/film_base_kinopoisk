'use client';

import Image from 'next/image';
import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog';

interface StillCardProps {
  still: {
    id: number;
    image_url: string;
    preview_url?: string;
    description?: string;
    image_width?: number;
    image_height?: number;
    type?: string;
  };
  className?: string;
}

export function StillCard({ still, className = '' }: StillCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(true);
  };

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  return (
    <Card className={`group overflow-hidden hover:shadow-lg transition-all duration-200 ${className}`}>
      <CardContent className="p-0">
        <Dialog>
          <DialogTrigger asChild>
            <div className="cursor-pointer">
              {/* Предварительный просмотр */}
              <div className="relative aspect-video overflow-hidden">
                {!imageLoaded && (
                  <Skeleton className="absolute inset-0 w-full h-full" />
                )}
                
                {still.image_url && !imageError ? (
                  <Image
                    src={still.image_url}
                    alt={still.description || 'Кадр из фильма'}
                    fill
                    className={`object-cover transition-transform duration-200 group-hover:scale-105 ${
                      !imageLoaded ? 'opacity-0' : 'opacity-100'
                    }`}
                    onLoad={handleImageLoad}
                    onError={handleImageError}
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    unoptimized={true}
                  />
                ) : (
                  <div className="w-full h-full bg-muted flex items-center justify-center">
                    <span className="text-muted-foreground text-sm">Изображение недоступно</span>
                  </div>
                )}

                {/* Индикатор типа */}
                {still.type && (
                  <Badge 
                    variant="secondary" 
                    className="absolute top-2 right-2 bg-background/80 backdrop-blur text-xs"
                  >
                    {still.type === 'still' ? 'Кадр' : 'Обои'}
                  </Badge>
                )}
              </div>
            </div>
          </DialogTrigger>
          
          {/* Полноразмерное изображение в модальном окне */}
          <DialogContent className="max-w-4xl p-0">
            {still.image_url && !imageError && (
              <div className="relative w-full h-auto max-h-[80vh] overflow-hidden">
                <Image
                  src={still.image_url}
                  alt={still.description || 'Кадр из фильма'}
                  width={still.image_width || 1920}
                  height={still.image_height || 1080}
                  className="w-full h-auto object-contain"
                  unoptimized={true}
                />
              </div>
            )}
            {still.description && (
              <div className="p-4">
                <p className="text-sm text-muted-foreground">{still.description}</p>
              </div>
            )}
          </DialogContent>
        </Dialog>

        {/* Информация о кадре */}
        {(still.description || still.image_width || still.image_height) && (
          <div className="p-3">
            {still.description && (
              <p className="text-sm text-muted-foreground line-clamp-2 mb-2">
                {still.description}
              </p>
            )}
            
            {(still.image_width || still.image_height) && (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                {still.image_width && (
                  <span>{still.image_width}px</span>
                )}
                {still.image_width && still.image_height && (
                  <span>×</span>
                )}
                {still.image_height && (
                  <span>{still.image_height}px</span>
                )}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// Скелетон для загрузки
export function StillCardSkeleton({ className }: { className?: string }) {
  return (
    <Card className={className}>
      <CardContent className="p-0">
        <div className="aspect-video">
          <Skeleton className="w-full h-full" />
        </div>
        <div className="p-3 space-y-2">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-3 w-1/2" />
        </div>
      </CardContent>
    </Card>
  );
}