'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { History, Clock, Play, Film } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { useUserInteractionsStore } from '@/store';
import { ROUTES } from '@/lib/config';

export default function HistoryPage() {
  useEffect(() => {
    console.log('History page loaded');
  }, []);

  // Временные данные для демонстрации
  const mockHistory = [
    {
      id: 1,
      film_id: 123,
      visited_at: new Date().toISOString(),
      film: {
        id: 123,
        title: "Интерстеллар",
        original_title: "Interstellar",
        poster: "",
        year: 2014,
        description: "Фантастическая драма о путешествиях в космосе",
      }
    },
    {
      id: 2,
      film_id: 456,
      visited_at: new Date(Date.now() - 86400000).toISOString(), // вчера
      film: {
        id: 456,
        title: "Начало",
        original_title: "Inception",
        poster: "",
        year: 2010,
        description: "Триллер о проникновении в сны",
      }
    }
  ];

  const currentHistory = mockHistory; // Временные данные

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return 'Сегодня';
    } else if (diffDays === 1) {
      return 'Вчера';
    } else if (diffDays < 7) {
      return `${diffDays} дн. назад`;
    } else {
      return date.toLocaleDateString('ru-RU');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <History className="h-8 w-8 text-blue-500" />
          <div>
            <h1 className="text-3xl font-bold">История просмотров</h1>
            <p className="text-muted-foreground">
              {currentHistory.length} фильмов просмотрено
            </p>
          </div>
        </div>
      </div>

      {/* Временное отображение без лоадера */}
      {currentHistory.length > 0 ? (
        <div className="space-y-4">
          {currentHistory.map((item) => (
            <Card key={item.id} className="group hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex gap-4">
                  {/* Постер */}
                  <div className="w-16 h-24 bg-muted rounded flex-shrink-0">
                    {item.film.poster ? (
                      <img 
                        src={item.film.poster} 
                        alt={item.film.title}
                        className="w-full h-full object-cover rounded"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <Film className="h-6 w-6 text-muted-foreground" />
                      </div>
                    )}
                  </div>

                  {/* Информация о фильме */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <Link 
                          href={ROUTES.FILM_DETAILS(item.film.id)}
                          className="block"
                        >
                          <h3 className="font-semibold text-lg hover:text-primary transition-colors line-clamp-1">
                            {item.film.title}
                          </h3>
                        </Link>
                        
                        {item.film.original_title && item.film.title !== item.film.original_title && (
                          <p className="text-sm text-muted-foreground line-clamp-1">
                            {item.film.original_title}
                          </p>
                        )}

                        {item.film.description && (
                          <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                            {item.film.description}
                          </p>
                        )}

                        <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                          {item.film.year && (
                            <span>{item.film.year}</span>
                          )}
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            <span>{formatDate(item.visited_at)}</span>
                          </div>
                        </div>
                      </div>

                      {/* Кнопка действия */}
                      <div className="flex-shrink-0">
                        <Button asChild size="sm">
                          <Link href={ROUTES.FILM_DETAILS(item.film.id)}>
                            <Play className="h-4 w-4 mr-2" />
                            Смотреть
                          </Link>
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <History className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">История пуста</h3>
          <p className="text-muted-foreground mb-6 max-w-md mx-auto">
            Здесь будет отображаться история просмотренных фильмов. 
            Начните смотреть фильмы, чтобы увидеть их здесь.
          </p>
          <Button asChild>
            <Link href={ROUTES.FILMS}>
              <Film className="h-4 w-4 mr-2" />
              Найти фильмы
            </Link>
          </Button>
        </div>
      )}

      {/* Полезные ссылки */}
      <div className="mt-12 pt-8 border-t">
        <h3 className="text-lg font-semibold mb-4">Управление историей</h3>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm">
            Очистить историю
          </Button>
          <Button variant="outline" size="sm">
            Экспорт данных
          </Button>
          <Button variant="outline" size="sm">
            Настройки приватности
          </Button>
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          История просмотров помогает нам предоставлять рекомендации и улучшать сервис.
        </p>
      </div>
    </div>
  );
}