'use client';

import { useEffect } from 'react';
import Image from 'next/image';
import { useAuth } from '@/hooks';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useUserInteractionsStore } from '@/store';
import { Calendar, Mail, User } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuth();
  const {
    bookmarks,
    userRatings,
    fetchBookmarks,
    fetchUserRatings
  } = useUserInteractionsStore();

  useEffect(() => {
    if (user) {
      fetchBookmarks();
      fetchUserRatings();
    }
  }, [user, fetchBookmarks, fetchUserRatings]);

  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <p className="text-muted-foreground">Загрузка профиля...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Заголовок профиля */}
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              {/* Аватар */}
              <Avatar className="w-24 h-24">
                <AvatarImage src={undefined} alt={user.email} />
                <AvatarFallback className="text-2xl">
                  {user.email?.charAt(0).toUpperCase() || 'U'}
                </AvatarFallback>
              </Avatar>

              {/* Информация о пользователе */}
              <div className="flex-1">
                <div>
                  <div className="flex items-center gap-4 mb-4">
                    <h1 className="text-3xl font-bold">{user.username}</h1>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4" />
                      <span>{user.email}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      <span>Создан: {new Date(user.created_at).toLocaleDateString('ru-RU')}</span>
                    </div>
                    {user.first_name?.trim() || user.last_name?.trim() ? (
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        <span>
                          {user.first_name?.trim() && user.last_name?.trim()
                            ? `${user.first_name.trim()} ${user.last_name.trim()}`
                            : user.first_name?.trim() || user.last_name?.trim()
                          }
                        </span>
                      </div>
                    ) : null}
                    <div className="flex items-center gap-2">
                      <User className="h-4 w-4" />
                      <span>ID: {user.id}</span>
                    </div>
                  </div>

                  <div className="flex gap-2 mt-4">
                    <Badge variant={user.is_verified ? "default" : "secondary"}>
                      {user.is_verified ? 'Подтвержден' : 'Не подтвержден'}
                    </Badge>
                    <Badge variant={user.is_superuser ? "default" : "outline"}>
                      {user.is_superuser ? 'Администратор' : 'Пользователь'}
                    </Badge>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Статистика */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Закладки</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{bookmarks.length}</div>
              <p className="text-xs text-muted-foreground">
                Сохраненных фильмов
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Оценки</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{userRatings.length}</div>
              <p className="text-xs text-muted-foreground">
                Поставленных оценок
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Средний рейтинг</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {userRatings.length > 0
                  ? (userRatings.reduce((sum, rating) => sum + rating.rating, 0) / userRatings.length).toFixed(1)
                  : '—'
                }
              </div>
              <p className="text-xs text-muted-foreground">
                Ваши оценки
              </p>
            </CardContent>
          </Card>
        </div>

        <Separator />

        {/* Последние оценки */}
        <Card>
          <CardHeader>
            <CardTitle>Последние оценки</CardTitle>
          </CardHeader>
          <CardContent>
            {userRatings.length > 0 ? (
              <div className="space-y-4">
                {userRatings.slice(0, 10).map((rating) => (
                  <div key={rating.id} className="flex items-center gap-4 p-3 border rounded-lg">
                    {/* Миниатюра фильма */}
                    <div className="w-16 h-20 bg-muted rounded-md overflow-hidden shrink-0">
                      {rating.film?.poster ? (
                        <Image
                          src={rating.film.poster}
                          alt={rating.film.title || 'Постер фильма'}
                          width={64}
                          height={80}
                          className="w-full h-full object-cover"
                          loading="lazy"
                          unoptimized
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <span className="text-xs text-muted-foreground">Постер</span>
                        </div>
                      )}
                    </div>

                    {/* Информация о фильме */}
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">
                        {rating.film?.title || `Фильм #${rating.film_id}`}
                      </p>
                      {rating.film?.year && (
                        <p className="text-sm text-muted-foreground">
                          {rating.film.year}
                        </p>
                      )}
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-sm font-medium">
                          Оценка: {rating.rating}/10
                        </span>
                      </div>
                    </div>

                    {/* Дата оценки */}
                    <div className="text-right shrink-0">
                      <p className="text-sm text-muted-foreground">
                        {new Date(rating.created_at).toLocaleDateString('ru-RU')}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-muted-foreground">У вас пока нет оценок</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}