'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { ArrowLeft, Calendar, MapPin, Award, Film } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import Link from 'next/link';
import { ROUTES } from '@/lib/config';
import { StuffAPI } from '@/lib/api';
import { Stuff } from '@/lib/types';
import { useHistoryStore } from '@/store';

export default function StuffDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const stuffId = parseInt(params.id as string);

  const [stuff, setStuff] = useState<Stuff | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { addToHistory } = useHistoryStore();

  const loadStuffDetails = useCallback(async () => {
    try {
      setIsLoading(true);
      setError('');
      const stuffData = await StuffAPI.getStuffById(stuffId);
      setStuff(stuffData);
    } catch (error: any) {
      console.error('Error loading stuff details:', error);
      setError('Участник не найден или произошла ошибка загрузки');
    } finally {
      setIsLoading(false);
    }
  }, [stuffId]);

  useEffect(() => {
    if (stuffId) {
      loadStuffDetails();
    }
  }, [stuffId, loadStuffDetails]);

  useEffect(() => {
    if (stuff) {
      addToHistory({
        id: stuff.id,
        type: 'person',
        title: stuff.name || stuff.original_name || 'Персона',
        image: stuff.image,
        description: stuff.career ? stuff.career.join(', ') : undefined,
      });
    }
  }, [stuff, addToHistory]);

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Skeleton className="h-8 w-48 mb-4" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <Skeleton className="aspect-square w-full" />
          </div>
          <div className="lg:col-span-2 space-y-6">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !stuff) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Button asChild variant="ghost">
            <Link href={ROUTES.FILMS}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              К списку фильмов
            </Link>
          </Button>
        </div>

        <Card className="text-center py-12">
          <CardContent>
            <p className="text-red-500 mb-4">{error}</p>
            <Button onClick={() => router.back()}>
              Вернуться назад
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Навигация */}
      <div className="mb-8">
        <Button asChild variant="ghost">
          <Link href={ROUTES.FILMS}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            К списку фильмов
          </Link>
        </Button>
      </div>

      {/* Основная информация об участнике */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Фото */}
        <div className="lg:col-span-1">
          <div className="sticky top-8">
            <Card className='p-0'>
              <CardContent className="p-0">
                {stuff.image ? (
                  <div className="aspect-square relative">
                    <Image
                      src={stuff.image}
                      alt={stuff.name || stuff.original_name || 'Участник'}
                      fill
                      className="object-contain rounded-t-lg"
                    />
                  </div>
                ) : (
                  <div className="aspect-square bg-muted flex items-center justify-center">
                    <span className="text-muted-foreground">Нет фото</span>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Детали */}
        <div className="lg:col-span-2 space-y-6">
          {/* Заголовок */}
          <div>
            <h1 className="text-3xl md:text-4xl font-bold mb-2">
              {stuff.name || stuff.original_name || 'Без имени'}
            </h1>
            {stuff.original_name && stuff.name !== stuff.original_name && (
              <p className="text-xl text-muted-foreground">
                {stuff.original_name}
              </p>
            )}
          </div>

          {/* Основная информация */}
          <div className="space-y-4">
            {stuff.age && (
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span>{stuff.age} лет</span>
              </div>
            )}

            {stuff.career_start_year && (
              <div className="flex items-center gap-2">
                <Award className="h-4 w-4 text-muted-foreground" />
                <span>
                  Карьера началась в {stuff.career_start_year}
                  {stuff.career_end_year && ` - ${stuff.career_end_year}`}
                </span>
              </div>
            )}

            {stuff.total_films && (
              <div className="flex items-center gap-2">
                <Film className="h-4 w-4 text-muted-foreground" />
                <span>Участвовал в {stuff.total_films} фильмах</span>
              </div>
            )}

            {stuff.birthplace && stuff.birthplace.length > 0 && (
              <div className="flex items-center gap-2">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <span>{stuff.birthplace[0]}</span>
              </div>
            )}
          </div>

          {/* Профессии */}
          {stuff.career && stuff.career.length > 0 && (
            <div>
              <h3 className="font-semibold mb-2">Профессии</h3>
              <div className="flex flex-wrap gap-2">
                {stuff.career.map((job, index) => (
                  <Badge key={index} variant="secondary">
                    {job}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Жанры */}
          {stuff.ganres && stuff.ganres.length > 0 && (
            <div>
              <h3 className="font-semibold mb-2">Жанры</h3>
              <div className="flex flex-wrap gap-2">
                {stuff.ganres.map((genre, index) => (
                  <Badge key={index} variant="outline">
                    {genre}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Подробная информация */}
      <Tabs defaultValue="biography" className="space-y-6">
        <TabsList>
          <TabsTrigger value="biography">Биография</TabsTrigger>
          <TabsTrigger value="personal">Личная информация</TabsTrigger>
        </TabsList>

        <TabsContent value="biography">
          <Card>
            <CardHeader>
              <CardTitle>Биография</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {stuff.name && stuff.original_name && (
                <div>
                  <h4 className="font-semibold mb-2">Имена</h4>
                  <p><strong>Имя:</strong> {stuff.name}</p>
                  <p><strong>Оригинальное имя:</strong> {stuff.original_name}</p>
                </div>
              )}

              {stuff.career && stuff.career.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Карьера</h4>
                  <p>{stuff.career.join(', ')}</p>
                </div>
              )}

              {stuff.height && (
                <div>
                  <h4 className="font-semibold mb-2">Рост</h4>
                  <p>{stuff.height}</p>
                </div>
              )}

              {stuff.birthday_day_month && (
                <div>
                  <h4 className="font-semibold mb-2">День рождения</h4>
                  <p>{stuff.birthday_day_month}</p>
                </div>
              )}

              {stuff.zodiac && (
                <div>
                  <h4 className="font-semibold mb-2">Знак зодиака</h4>
                  <p>{stuff.zodiac}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="personal">
          <Card>
            <CardHeader>
              <CardTitle>Личная информация</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {stuff.birthplace && stuff.birthplace.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Место рождения</h4>
                  <ul className="list-disc list-inside">
                    {stuff.birthplace.map((place, index) => (
                      <li key={index}>{place}</li>
                    ))}
                  </ul>
                </div>
              )}

              {stuff.spouse && stuff.spouse.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Супруги</h4>
                  <ul className="list-disc list-inside">
                    {stuff.spouse.map((spouse, index) => (
                      <li key={index}>{spouse}</li>
                    ))}
                  </ul>
                </div>
              )}

              {stuff.children && stuff.children.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Дети</h4>
                  <ul className="list-disc list-inside">
                    {stuff.children.map((child, index) => (
                      <li key={index}>{child}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}