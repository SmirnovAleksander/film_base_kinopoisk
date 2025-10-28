'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { Play, Star, TrendingUp, Film, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FilmCard, FilmCardSkeleton } from '@/components/film/film-card';
import { useAuth } from '@/hooks/use-auth';
import { useFilmsStore } from '@/store';
import { ROUTES } from '@/lib/config';

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const { 
    films, 
    fetchFilms, 
    isLoading 
  } = useFilmsStore();

  useEffect(() => {
    fetchFilms(1);
  }, [fetchFilms]);

  const featuredFilms = films.slice(0, 6);
  const latestFilms = films.slice(6, 12);

  return (
    <div className="min-h-screen bg-background">
      {/* Героический блок */}
      <section className="relative bg-gradient-to-br from-primary/10 via-background to-secondary/10 py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              Ваша персональная база фильмов
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Откройте для себя лучшие фильмы, оценивайте их, создавайте закладки и получайте персонализированные рекомендации
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg" className="text-lg">
                <Link href={ROUTES.FILMS}>
                  <Film className="mr-2 h-5 w-5" />
                  Исследовать фильмы
                </Link>
              </Button>
              {!isAuthenticated && (
                <Button asChild variant="outline" size="lg" className="text-lg">
                  <Link href={ROUTES.REGISTER}>
                    Присоединиться бесплатно
                  </Link>
                </Button>
              )}
            </div>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        {/* Возможности */}
        <section className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Возможности платформы</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Всё что нужно для управления вашей кинотекой
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="text-center">
              <CardHeader>
                <Star className="h-8 w-8 mx-auto text-yellow-500 mb-2" />
                <CardTitle className="text-lg">Оценки и рейтинги</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Оценивайте фильмы по 10-балльной шкале и создавайте свою коллекцию
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Heart className="h-8 w-8 mx-auto text-red-500 mb-2" />
                <CardTitle className="text-lg">Закладки</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Сохраняйте любимые фильмы в личную коллекцию для быстрого доступа
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <TrendingUp className="h-8 w-8 mx-auto text-blue-500 mb-2" />
                <CardTitle className="text-lg">Рекомендации</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Получайте персонализированные рекомендации на основе ваших предпочтений
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Play className="h-8 w-8 mx-auto text-green-500 mb-2" />
                <CardTitle className="text-lg">История просмотров</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Отслеживайте свою киноисторию и не теряйте интересные фильмы
                </p>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Рекомендуемые фильмы */}
        <section className="mb-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold">Рекомендуемые фильмы</h2>
            <Button asChild variant="outline">
              <Link href={ROUTES.FILMS}>Смотреть все</Link>
            </Button>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {Array.from({ length: 6 }).map((_, i) => (
                <FilmCardSkeleton key={i} />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {featuredFilms.map((film) => (
                <FilmCard key={film.id} film={film} />
              ))}
            </div>
          )}
        </section>

        {/* Новые поступления */}
        <section className="mb-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold">Новые поступления</h2>
            <Button asChild variant="outline">
              <Link href={ROUTES.FILMS}>Смотреть все</Link>
            </Button>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {Array.from({ length: 6 }).map((_, i) => (
                <FilmCardSkeleton key={i} />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {latestFilms.map((film) => (
                <FilmCard key={film.id} film={film} />
              ))}
            </div>
          )}
        </section>

        {/* Call to Action */}
        {!isAuthenticated && (
          <section className="text-center py-16 bg-muted/50 rounded-lg">
            <h2 className="text-3xl font-bold mb-4">Начните прямо сейчас</h2>
            <p className="text-muted-foreground mb-8 max-w-md mx-auto">
              Создайте аккаунт и откройте для себя мир персонализированного кинопоиска
            </p>
            <Button asChild size="lg">
              <Link href={ROUTES.REGISTER}>
                Зарегистрироваться бесплатно
              </Link>
            </Button>
          </section>
        )}
      </div>
    </div>
  );
}
