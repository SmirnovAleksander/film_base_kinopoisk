'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useUserInteractionsStore } from '@/store';
import { FilmCard, FilmCardSkeleton } from '@/components/film/film-card';
import { Edit, Calendar, Mail, User, Settings } from 'lucide-react';

export default function ProfilePage() {
  const { user, updateUser, isLoading } = useAuth();
  const { 
    bookmarks, 
    userRatings, 
    fetchBookmarks, 
    fetchUserRatings 
  } = useUserInteractionsStore();

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    username: user?.username || '',
  });
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        username: user.username || '',
      });
      fetchBookmarks();
      fetchUserRatings();
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsUpdating(true);

    try {
      await updateUser(formData);
      setIsEditing(false);
    } catch (error) {
      console.error('Update profile error:', error);
    } finally {
      setIsUpdating(false);
    }
  };

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
                {isEditing ? (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="first_name">Имя</Label>
                        <Input
                          id="first_name"
                          value={formData.first_name}
                          onChange={(e) => setFormData(prev => ({ ...prev, first_name: e.target.value }))}
                          disabled={isUpdating}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="last_name">Фамилия</Label>
                        <Input
                          id="last_name"
                          value={formData.last_name}
                          onChange={(e) => setFormData(prev => ({ ...prev, last_name: e.target.value }))}
                          disabled={isUpdating}
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="username">Имя пользователя</Label>
                      <Input
                        id="username"
                        value={formData.username}
                        onChange={(e) => setFormData(prev => ({ ...prev, username: e.target.value }))}
                        disabled={isUpdating}
                      />
                    </div>
                    <div className="flex gap-2">
                      <Button type="submit" disabled={isUpdating}>
                        {isUpdating ? 'Сохранение...' : 'Сохранить'}
                      </Button>
                      <Button 
                        type="button" 
                        variant="outline" 
                        onClick={() => {
                          setIsEditing(false);
                          setFormData({
                            first_name: user.first_name || '',
                            last_name: user.last_name || '',
                            username: user.username || '',
                          });
                        }}
                        disabled={isUpdating}
                      >
                        Отмена
                      </Button>
                    </div>
                  </form>
                ) : (
                  <div>
                    <div className="flex items-center gap-4 mb-4">
                      <h1 className="text-3xl font-bold">
                        {user.first_name && user.last_name 
                          ? `${user.first_name} ${user.last_name}`
                          : user.email
                        }
                      </h1>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setIsEditing(true)}
                      >
                        <Edit className="h-4 w-4 mr-2" />
                        Редактировать
                      </Button>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-2">
                        <Mail className="h-4 w-4" />
                        <span>{user.email}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        <span>@{user.username || 'не указано'}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        <span>С {new Date(user.created_at).toLocaleDateString('ru-RU')}</span>
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
                )}
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

        {/* Последние закладки */}
        <Card>
          <CardHeader>
            <CardTitle>Последние закладки</CardTitle>
          </CardHeader>
          <CardContent>
            {bookmarks.length > 0 ? (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {bookmarks.slice(0, 12).map((bookmark) => (
                  <div key={bookmark.id} className="aspect-[2/3]">
                    {/* Временная заглушка */}
                    <div className="w-full h-full bg-muted rounded-md flex items-center justify-center">
                      <span className="text-xs text-muted-foreground">ID: {bookmark.film_id}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-muted-foreground">У вас пока нет закладок</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Последние оценки */}
        <Card>
          <CardHeader>
            <CardTitle>Последние оценки</CardTitle>
          </CardHeader>
          <CardContent>
            {userRatings.length > 0 ? (
              <div className="space-y-4">
                {userRatings.slice(0, 10).map((rating) => (
                  <div key={rating.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">Фильм ID: {rating.film_id}</p>
                      <p className="text-sm text-muted-foreground">
                        Оценка: {rating.rating}/10
                      </p>
                    </div>
                    <div className="text-right">
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