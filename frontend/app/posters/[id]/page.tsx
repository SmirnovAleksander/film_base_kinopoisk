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
import type { FilmStills } from '@/lib/types/film.types';

export default function PostersPage() {
  const params = useParams();
  const filmId = parseInt(params.id as string);
  
  const { currentFilm } = useFilmsStore();
  const [filmStills, setFilmStills] = useState<FilmStills>({ stills: [], wall: [] });
  const [isLoadingStills, setIsLoadingStills] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

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
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
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
          {(filmStills.stills.length > 0 || filmStills.wall.length > 0) && (
            <div className="flex gap-2">
              {filmStills.stills.length > 0 && (
                <Badge variant="secondary">
                  Кадры: {filmStills.stills.length}
                </Badge>
              )}
              {filmStills.wall.length > 0 && (
                <Badge variant="secondary">
                  Обои: {filmStills.wall.length}
                </Badge>
              )}
            </div>
          )}
        </div>

        <Separator />

        {/* Контент */}
        {(filmStills.stills.length > 0 || filmStills.wall.length > 0) ? (
          <Tabs defaultValue="stills" className="space-y-8">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="stills" className="flex items-center gap-2">
                <ImageIcon className="h-4 w-4" />
                Кадры из фильма {filmStills.stills.length > 0 && `(${filmStills.stills.length})`}
              </TabsTrigger>
              <TabsTrigger value="wall" className="flex items-center gap-2">
                <Maximize2 className="h-4 w-4" />
                Обои {filmStills.wall.length > 0 && `(${filmStills.wall.length})`}
              </TabsTrigger>
            </TabsList>

            <TabsContent value="stills" className="space-y-6">
              {filmStills.stills.length > 0 ? (
                <div className={
                  viewMode === 'grid' 
                    ? 'grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4'
                    : 'space-y-4'
                }>
                  {filmStills.stills.map((still) => (
                    <div key={still.id}>
                      <StillCard still={still} className={viewMode === 'list' ? 'w-full max-w-md mx-auto' : ''} />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <ImageIcon className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <p className="text-muted-foreground text-lg mb-2">
                    Кадры из фильма отсутствуют
                  </p>
                  <p className="text-muted-foreground">
                    В ближайшее время будут добавлены изображения
                  </p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="wall" className="space-y-6">
              {filmStills.wall.length > 0 ? (
                <div className={
                  viewMode === 'grid' 
                    ? 'grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4'
                    : 'space-y-4'
                }>
                  {filmStills.wall.map((wall) => (
                    <div key={wall.id}>
                      <StillCard still={wall} className={viewMode === 'list' ? 'w-full max-w-md mx-auto' : ''} />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Maximize2 className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <p className="text-muted-foreground text-lg mb-2">
                    Обои отсутствуют
                  </p>
                  <p className="text-muted-foreground">
                    В ближайшее время будут добавлены изображения
                  </p>
                </div>
              )}
            </TabsContent>
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