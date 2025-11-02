'use client';

import Image from 'next/image';
import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog';

interface StillCardProps {
  still: {
    id: string;
    original: string;
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
    <Card className={`group overflow-hidden hover:shadow-lg transition-all duration-200 p-0 ${className}`}>
      <CardContent className="p-0">
        <Dialog>
          <DialogTrigger asChild>
            <div className="cursor-pointer">
              {/* Предварительный просмотр */}
              <div className="relative aspect-video overflow-hidden">
                {!imageLoaded && (
                  <Skeleton className="absolute inset-0 w-full h-full" />
                )}
                
                {still.original && !imageError ? (
                  <Image
                    src={still.original}
                    alt={`Кадр из фильма ${still.id}`}
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
              </div>
            </div>
          </DialogTrigger>
        </Dialog>
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
      </CardContent>
    </Card>
  );
}