'use client';

import Image from 'next/image';
import { useState } from 'react';
import { X } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogTrigger, DialogContent, DialogTitle, DialogClose } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

interface StillCardProps {
  still: {
    id: string;
    original: string;
  };
  className?: string;
  unoptimized?: boolean;
}

export function StillCard({ still, className = '', unoptimized = false }: StillCardProps) {
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
                    unoptimized={unoptimized}
                  />
                ) : (
                  <div className="w-full h-full bg-muted flex items-center justify-center">
                    <span className="text-muted-foreground text-sm">Изображение недоступно</span>
                  </div>
                )}
              </div>
            </div>
          </DialogTrigger>
          {still.original && !imageError && (
            <DialogContent 
              className="w-[95vw] h-[95vh] max-w-[95vw] max-h-[95vh] p-2 bg-transparent border-none focus:outline-none flex items-center justify-center"
              showCloseButton={false}
            >
              <DialogTitle className="sr-only">
                Кадр из фильма {still.id}
              </DialogTitle>
              <div className="relative w-full h-full flex items-center justify-center">
                <div className="relative inline-block">
                  <Image
                    src={still.original}
                    alt={`Кадр из фильма ${still.id}`}
                    width={1920}
                    height={1080}
                    className="max-w-[93vw] max-h-[93vh] w-auto h-auto object-contain rounded-lg"
                    unoptimized={true}
                    priority
                  />
                  <DialogClose asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute top-2 right-2 bg-black/50 hover:bg-black/70 text-white rounded-full w-10 h-10 z-10 shadow-lg"
                    >
                      <X className="h-5 w-5" />
                      <span className="sr-only">Закрыть</span>
                    </Button>
                  </DialogClose>
                </div>
              </div>
            </DialogContent>
          )}
        </Dialog>
      </CardContent>
    </Card>
  );
}

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