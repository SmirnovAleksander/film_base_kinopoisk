'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import { 
  ArrowLeft, 
  Calendar, 
  Clock, 
  Star, 
  Heart, 
  MessageSquare,
  Share,
  ExternalLink,
  MapPin,
  Users,
  TrendingUp
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import Link from 'next/link';
import { FilmCard, FilmCardSkeleton } from '@/components/film/film-card';
import { StarRating } from '@/components/film/star-rating';
import { useFilmsStore, useUserInteractionsStore } from '@/store';
import { ROUTES } from '@/lib/config';
import { FilmsAPI } from '@/lib/api';

export default function FilmDetailsPage() {
  const params = useParams();
  const filmId = parseInt(params.id as string);
  
  const { currentFilm, fetchFilmDetails, isLoading } = useFilmsStore();
  const { 
    fetchFilmComments, 
    addComment, 
    comments,
    bookmarkedFilmIds,
    addBookmark,
    removeBookmark,
    isAddingBookmark,
    isLoadingComments,
    isAddingComment
  } = useUserInteractionsStore();

  const [newComment, setNewComment] = useState('');
  const [activeTab, setActiveTab] = useState('details');
  const [filmStuff, setFilmStuff] = useState<any[]>([]);
  const [isLoadingStuff, setIsLoadingStuff] = useState(false);

  useEffect(() => {
    if (filmId) {
      fetchFilmDetails(filmId);
      fetchFilmComments(filmId);
      loadFilmStuff();
    }
  }, [filmId]);

  const loadFilmStuff = async () => {
    try {
      setIsLoadingStuff(true);
      const stuff = await FilmsAPI.getFilmStuff(filmId);
      setFilmStuff(stuff);
    } catch (error) {
      console.error('Error loading film stuff:', error);
    } finally {
      setIsLoadingStuff(false);
    }
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    await addComment(filmId, newComment.trim());
    setNewComment('');
  };

  const handleBookmarkToggle = async () => {
    const isBookmarked = bookmarkedFilmIds.has(filmId);
    if (isBookmarked) {
      await removeBookmark(filmId);
    } else {
      await addBookmark(filmId);
    }
  };

  const isBookmarked = bookmarkedFilmIds.has(filmId);

  if (isLoading || !currentFilm) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Skeleton className="h-8 w-48 mb-4" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <Skeleton className="aspect-[2/3] w-full" />
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

      {/* Основная информация о фильме */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Постер */}
        <div className="lg:col-span-1">
          <div className="sticky top-8">
            <Card>
              <CardContent className="p-0">
                {currentFilm.poster ? (
                  <div className="aspect-[2/3] relative">
                    <Image
                      src={currentFilm.poster}
                      alt={currentFilm.title || 'Без названия'}
                      fill
                      className="object-cover rounded-t-lg"
                      sizes="(max-width: 768px) 100vw, 33vw"
                    />
                  </div>
                ) : (
                  <div className="aspect-[2/3] bg-muted flex items-center justify-center">
                    <span className="text-muted-foreground">Нет постера</span>
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
              {currentFilm.title || currentFilm.original_title || 'Без названия'}
            </h1>
            {currentFilm.original_title && currentFilm.title !== currentFilm.original_title && (
              <p className="text-xl text-muted-foreground">
                {currentFilm.original_title}
              </p>
            )}
            {currentFilm.tagline && (
              <p className="text-lg italic text-muted-foreground mt-2">
                "{currentFilm.tagline}"
              </p>
            )}
          </div>

          {/* Кнопки действий */}
          <div className="flex flex-wrap gap-2">
            <StarRating 
              filmId={filmId} 
              interactive={true}
              size="lg"
            />
            <Button
              variant={isBookmarked ? "default" : "outline"}
              onClick={handleBookmarkToggle}
              disabled={isAddingBookmark}
            >
              <Heart className={`h-4 w-4 mr-2 ${isBookmarked ? 'fill-current' : ''}`} />
              {isBookmarked ? 'В закладках' : 'В закладки'}
            </Button>
            <Button variant="outline">
              <Share className="h-4 w-4 mr-2" />
              Поделиться
            </Button>
          </div>

          {/* Метаинформация */}
          <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
            {currentFilm.year && (
              <div className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                <span>{currentFilm.year}</span>
              </div>
            )}
            {currentFilm.duration && (
              <div className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                <span>{currentFilm.duration}</span>
              </div>
            )}
            {currentFilm.content_rating && (
              <Badge variant="secondary">
                {currentFilm.content_rating}
              </Badge>
            )}
          </div>

          {/* Рейтинги */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {currentFilm.rating_kp && (
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2">
                    <Star className="h-4 w-4 text-yellow-500" />
                    <span className="font-medium">Кинопоиск</span>
                  </div>
                  <p className="text-2xl font-bold">{currentFilm.rating_kp}</p>
                  <p className="text-xs text-muted-foreground">
                    {currentFilm.kp_votes_count} голосов
                  </p>
                </CardContent>
              </Card>
            )}
            {currentFilm.rating_imdb && (
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2">
                    <Star className="h-4 w-4 text-yellow-500" />
                    <span className="font-medium">IMDB</span>
                  </div>
                  <p className="text-2xl font-bold">{currentFilm.rating_imdb}</p>
                  <p className="text-xs text-muted-foreground">
                    {currentFilm.imdb_votes_count} голосов
                  </p>
                </CardContent>
              </Card>
            )}
            {currentFilm.user_rating && (
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-blue-500" />
                    <span className="font-medium">Пользователи</span>
                  </div>
                  <p className="text-2xl font-bold">{currentFilm.user_rating}</p>
                  <p className="text-xs text-muted-foreground">
                    {currentFilm.user_rating_count} оценок
                  </p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Жанры и страны */}
          <div className="space-y-4">
            {currentFilm.genres.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Жанры</h3>
                <div className="flex flex-wrap gap-2">
                  {currentFilm.genres.map((genre) => (
                    <Badge key={genre.id} variant="secondary">
                      {genre.name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
            {currentFilm.countries.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Страны</h3>
                <div className="flex flex-wrap gap-2">
                  {currentFilm.countries.map((country) => (
                    <Badge key={country.id} variant="outline">
                      <MapPin className="h-3 w-3 mr-1" />
                      {country.name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Подробная информация */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="details">Описание</TabsTrigger>
          <TabsTrigger value="crew">Участники</TabsTrigger>
          <TabsTrigger value="similar">Похожие</TabsTrigger>
          <TabsTrigger value="comments">
            Комментарии {comments.length > 0 && `(${comments.length})`}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="details" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Описание</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {currentFilm.full_description && (
                <div>
                  <h4 className="font-semibold mb-2">Полное описание</h4>
                  <p className="text-muted-foreground leading-relaxed">
                    {currentFilm.full_description}
                  </p>
                </div>
              )}
              
              {currentFilm.description && (
                <div>
                  <h4 className="font-semibold mb-2">Краткое описание</h4>
                  <p className="text-muted-foreground leading-relaxed">
                    {currentFilm.description}
                  </p>
                </div>
              )}

              {/* Дополнительная информация */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
                {currentFilm.budget && (
                  <div>
                    <h5 className="font-medium">Бюджет</h5>
                    <p className="text-muted-foreground">{currentFilm.budget}</p>
                  </div>
                )}
                {currentFilm.usa_box_office && (
                  <div>
                    <h5 className="font-medium">Сборы в США</h5>
                    <p className="text-muted-foreground">{currentFilm.usa_box_office}</p>
                  </div>
                )}
                {currentFilm.rus_box_office && (
                  <div>
                    <h5 className="font-medium">Сборы в России</h5>
                    <p className="text-muted-foreground">{currentFilm.rus_box_office}</p>
                  </div>
                )}
                {currentFilm.ru_premiere && (
                  <div>
                    <h5 className="font-medium">Премьера в России</h5>
                    <p className="text-muted-foreground">{currentFilm.ru_premiere}</p>
                  </div>
                )}
                {currentFilm.world_premiere && (
                  <div>
                    <h5 className="font-medium">Мировая премьера</h5>
                    <p className="text-muted-foreground">{currentFilm.world_premiere}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="crew">
          <Card>
            <CardHeader>
              <CardTitle>Участники</CardTitle>
            </CardHeader>
            <CardContent>
              {isLoadingStuff ? (
                <div className="space-y-4">
                  {Array.from({ length: 6 }).map((_, i) => (
                    <div key={i} className="flex items-center space-x-4">
                      <Skeleton className="h-16 w-16 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-48" />
                        <Skeleton className="h-3 w-32" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : filmStuff.length > 0 ? (
                <div className="space-y-4">
                  {filmStuff.map((person) => (
                    <div key={person.id} className="flex items-center space-x-4 p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                      {person.image ? (
                        <img
                          src={person.image}
                          alt={person.name || person.original_name}
                          className="h-16 w-16 rounded-full object-cover"
                        />
                      ) : (
                        <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                          <span className="text-muted-foreground text-sm">Нет фото</span>
                        </div>
                      )}
                      <div className="flex-1">
                        <h3 className="font-semibold">
                          <Link 
                            href={`/stuff/${person.id}`}
                            className="hover:text-blue-600 transition-colors"
                          >
                            {person.name || person.original_name}
                          </Link>
                        </h3>
                        {person.original_name && person.name !== person.original_name && (
                          <p className="text-sm text-muted-foreground">{person.original_name}</p>
                        )}
                        {person.career && person.career.length > 0 && (
                          <p className="text-sm text-muted-foreground">
                            {person.career.slice(0, 3).join(', ')}
                            {person.career.length > 3 && '...'}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-center text-muted-foreground py-8">
                  Информация об участниках не найдена.
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="similar">
          <Card>
            <CardHeader>
              <CardTitle>
                <TrendingUp className="h-5 w-5 inline mr-2" />
                Похожие фильмы
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {Array.from({ length: 6 }).map((_, i) => (
                  <FilmCardSkeleton key={i} />
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="comments" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Комментарии</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Форма добавления комментария */}
              <form onSubmit={handleCommentSubmit} className="space-y-4">
                <textarea
                  placeholder="Напишите ваш комментарий..."
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  className="w-full min-h-[100px] p-3 border rounded-md resize-none"
                  disabled={isAddingComment}
                />
                <Button type="submit" disabled={!newComment.trim() || isAddingComment}>
                  <MessageSquare className="h-4 w-4 mr-2" />
                  {isAddingComment ? 'Отправка...' : 'Отправить комментарий'}
                </Button>
              </form>

              <Separator />

              {/* Список комментариев */}
              {isLoadingComments ? (
                <div className="space-y-4">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <div key={i} className="space-y-2">
                      <Skeleton className="h-4 w-1/3" />
                      <Skeleton className="h-16 w-full" />
                      <Skeleton className="h-3 w-1/4" />
                    </div>
                  ))}
                </div>
              ) : comments.length > 0 ? (
                <div className="space-y-4">
                  {comments.map((comment) => (
                    <div key={comment.id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">
                          Пользователь #{comment.user_id}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {new Date(comment.created_at).toLocaleDateString('ru-RU')}
                        </span>
                      </div>
                      <p className="text-muted-foreground">{comment.content}</p>
                      {comment.is_edited && (
                        <p className="text-xs text-muted-foreground mt-1">
                          (изменено)
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-center text-muted-foreground py-8">
                  Комментариев пока нет. Будьте первым!
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}