'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { History, Clock, Play, Film, Trash2, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useHistoryStore } from '@/store';
import { ROUTES } from '@/lib/config';

export default function HistoryPage() {
  const { items, removeFromHistory, clearHistory } = useHistoryStore();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

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

  const handleClearHistory = () => {
    if (confirm('Вы уверены, что хотите очистить всю историю просмотров?')) {
      clearHistory();
    }
  };

  if (!mounted) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <History className="h-8 w-8 text-blue-500" />
          <div>
            <h1 className="text-3xl font-bold">История просмотров</h1>
            <p className="text-muted-foreground">
              {items.length} записей
            </p>
          </div>
        </div>
      </div>

      {items.length > 0 ? (
        <div className="space-y-4">
          {items.map((item) => (
            <Card key={`${item.type}-${item.id}`} className="group hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex gap-4">
                  {/* Постер/Фото */}
                  <div className="w-16 h-24 bg-muted rounded shrink-0 overflow-hidden">
                    {item.image ? (
                      <img
                        src={item.image}
                        alt={item.title}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        {item.type === 'film' ? (
                          <Film className="h-6 w-6 text-muted-foreground" />
                        ) : (
                          <User className="h-6 w-6 text-muted-foreground" />
                        )}
                      </div>
                    )}
                  </div>

                  {/* Информация */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <Link
                          href={item.type === 'film' ? ROUTES.FILM_DETAILS(item.id) : ROUTES.STUFF_DETAILS(item.id)}
                          className="block"
                        >
                          <h3 className="font-semibold text-lg hover:text-primary transition-colors line-clamp-1">
                            {item.title}
                          </h3>
                        </Link>

                        {item.description && (
                          <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                            {item.description}
                          </p>
                        )}

                        <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                          <span className="capitalize">{item.type === 'film' ? 'Фильм' : 'Персона'}</span>
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            <span>{formatDate(item.visitedAt)}</span>
                          </div>
                        </div>
                      </div>

                      {/* Кнопки действий */}
                      <div className="flex gap-2 shrink-0">
                        <Button asChild size="sm">
                          <Link href={item.type === 'film' ? ROUTES.FILM_DETAILS(item.id) : ROUTES.STUFF_DETAILS(item.id)}>
                            <Play className="h-4 w-4 mr-2" />
                            Перейти
                          </Link>
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => removeFromHistory(item.id, item.type)}
                        >
                          <Trash2 className="h-4 w-4" />
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
            Здесь будет отображаться история просмотренных фильмов и актеров.
            Начните смотреть фильмы и изучать профили участников, чтобы увидеть их здесь.
          </p>
          <Button asChild>
            <Link href={ROUTES.FILMS}>
              <Film className="h-4 w-4 mr-2" />
              Найти фильмы
            </Link>
          </Button>
        </div>
      )}

      {/* Управление историей */}
      {items.length > 0 && (
        <div className="mt-12 pt-8 border-t">
          <h3 className="text-lg font-semibold mb-4">Управление историей</h3>
          <div className="flex flex-wrap gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleClearHistory}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Очистить историю
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            История сохраняется локально в вашем браузере (последние 20 записей).
          </p>
        </div>
      )}
    </div>
  );
}