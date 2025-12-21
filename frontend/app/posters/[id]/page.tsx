'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { 
  ArrowLeft, 
  Image as ImageIcon,
  Maximize2,
  Grid3X3,
  List
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import Link from 'next/link';
import { StillCard, StillCardSkeleton } from '@/components/film';
import { FilmsAPI } from '@/lib/api';
import { useFilmsStore } from '@/store';
import { ROUTES } from '@/lib/config';
import type { FilmStills, FilmStillType } from '@/lib/types/film.types';

// Названия категорий на русском
const getCategoryLabel = (type: FilmStillType): string => {
  const labels: Record<FilmStillType, string> = {
    stills: 'Кадры из фильма',
    wall: 'Обои',
    shooting: 'Со съемок',
    screenshots: 'Скриншоты'
  };
  return labels[type];
};

export default function PostersPage() {
  const params = useParams();
  const filmId = parseInt(params.id as string);
  
  const { currentFilm } = useFilmsStore();
  const [filmStills, setFilmStills] = useState<FilmStills>({});
  const [isLoadingStills, setIsLoadingStills] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Получаем доступные типы (только те, которые есть в данных)
  const availableTypes = Object.keys(filmStills).filter(key => 
    filmStills[key as keyof FilmStills] && filmStills[key as keyof FilmStills]!.length > 0
  ) as Array<keyof FilmStills>;
  
  // Получаем общее количество всех изображений
  const totalCount = availableTypes.reduce((sum, type) => 
    sum + (filmStills[type]?.length || 0), 0
  );

  useEffect(() => {
    if (filmId) {
      loadFilmStills();
    }
  }, [filmId]);

  const loadFilmStills = async () => {
    try {
      setIsLoadingStills(true);
      const stills = await FilmsAPI.getFilmStills(filmId);
      setFilmStills(stills);
    } catch (error) {
      console.error('Error loading film stills:', error);
    } finally {
      setIsLoadingStills(false);
    }
  };

  if (isLoadingStills) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Skeleton className="h-8 w-48 mb-4" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="space-y-8">
          {Array.from({ length: 2 }).map((_, i) => (
            <Card key={i} className="border-0 shadow-xl">
              <CardHeader>
                <Skeleton className="h-8 w-64" />
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {Array.from({ length: 12 }).map((_, j) => (
                    <StillCardSkeleton key={j} />
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-background via-background to-muted/30">
      <div className="container mx-auto px-4 py-8 space-y-8">
        {/* Навигация */}
        <div className="mb-8">
          <Button asChild variant="ghost" className="text-muted-foreground hover:text-foreground">
            <Link href={ROUTES.FILM_DETAILS(filmId)}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              К фильму
            </Link>
          </Button>
        </div>

        {/* Заголовок */}
        <div className="space-y-4">
          <h1 className="text-3xl md:text-4xl font-bold bg-linear-to-r from-foreground to-foreground/80 bg-clip-text text-transparent">
            Галерея изображений
          </h1>
          {currentFilm && (
            <p className="text-xl text-muted-foreground">
              {currentFilm.title || currentFilm.original_title || 'Фильм'}
            </p>
          )}
        </div>

        {/* Переключатель вида */}
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Button
              variant={viewMode === 'grid' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('grid')}
            >
              <Grid3X3 className="h-4 w-4 mr-2" />
              Сетка
            </Button>
            <Button
              variant={viewMode === 'list' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('list')}
            >
              <List className="h-4 w-4 mr-2" />
              Список
            </Button>
          </div>
          
          {/* Статистика */}
          {availableTypes.length > 0 && (
            <div className="flex gap-2 flex-wrap">
              {availableTypes.map((type) => (
                <Badge key={type} variant="secondary">
                  {getCategoryLabel(type as FilmStillType)}: {filmStills[type]?.length || 0}
                </Badge>
              ))}
            </div>
          )}
        </div>

        <Separator />

        {/* Контент */}
        {availableTypes.length > 0 ? (
          <Tabs defaultValue={availableTypes[0] as string} className="space-y-8">
            <TabsList className={`grid w-full ${availableTypes.length === 1 ? 'grid-cols-1' : availableTypes.length === 2 ? 'grid-cols-2' : availableTypes.length === 3 ? 'grid-cols-3' : 'grid-cols-4'}`}>
              {availableTypes.map((type) => (
                <TabsTrigger key={type} value={type} className="flex items-center gap-2">
                  <ImageIcon className="h-4 w-4" />
                  {getCategoryLabel(type as FilmStillType)} ({filmStills[type]?.length || 0})
                </TabsTrigger>
              ))}
            </TabsList>

            {availableTypes.map((type) => (
              <TabsContent key={type} value={type} className="space-y-6">
                {filmStills[type] && filmStills[type]!.length > 0 ? (
                  <div className={
                    viewMode === 'grid' 
                      ? 'grid grid-cols-1 sm:grid-cols-3 gap-4'
                      : 'space-y-4'
                  }>
                    {filmStills[type]!.map((still) => (
                      <div key={still.id}>
                        <StillCard 
                          still={still} 
                          className={viewMode === 'list' ? 'w-full max-w-4xl mx-auto' : ''}
                          unoptimized={viewMode === 'list'}
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <ImageIcon className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <p className="text-muted-foreground text-lg mb-2">
                      {getCategoryLabel(type as FilmStillType)} отсутствуют
                    </p>
                    <p className="text-muted-foreground">
                      В ближайшее время будут добавлены изображения
                    </p>
                  </div>
                )}
              </TabsContent>
            ))}
          </Tabs>
        ) : (
          <div className="text-center py-12">
            <ImageIcon className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground text-lg mb-2">
              Изображения не найдены
            </p>
            <p className="text-muted-foreground">
              Попробуйте вернуться к фильму позже
            </p>
          </div>
        )}
      </div>
    </div>
  );
}