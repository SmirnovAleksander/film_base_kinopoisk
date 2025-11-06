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
  MapPin,
  Users,
  TrendingUp,
  Play,
  Eye,
  Edit,
  Trash2,
  Send,
  Image as ImageIcon
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import Link from 'next/link';
import { FilmCard, FilmCardSkeleton, MiniPersonCard, StillCard, StillCardSkeleton } from '@/components/film';
import { StarRating } from '@/components/film';
import { useFilmsStore, useUserInteractionsStore, useAuthStore } from '@/store';
import { useAuth } from '@/hooks/use-auth';
import { toast } from 'sonner';
import { ROUTES } from '@/lib/config';
import { FilmsAPI } from '@/lib/api';
import type { FilmStills } from '@/lib/types/film.types';

export default function FilmDetailsPage() {
  const params = useParams();
  const filmId = parseInt(params.id as string);
  
  const { currentFilm, fetchFilmDetails, isLoading } = useFilmsStore();
  const {
    comments,
    fetchFilmComments,
    addComment,
    updateComment,
    deleteComment,
    bookmarkedFilmIds,
    addBookmark,
    removeBookmark,
    isAddingBookmark,
    isLoadingComments,
    isAddingComment
  } = useUserInteractionsStore();
  const { user } = useAuthStore();
  const { isAuthenticated } = useAuth();

  const [newComment, setNewComment] = useState('');
  const [filmStuff, setFilmStuff] = useState<any[]>([]);
  const [isLoadingStuff, setIsLoadingStuff] = useState(false);
  const [filmStills, setFilmStills] = useState<FilmStills>({ stills: [], wall: [] });
  const [isLoadingStills, setIsLoadingStills] = useState(false);
  const [recommendedFilms, setRecommendedFilms] = useState<any[]>([]);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false);
  const [similarFilms, setSimilarFilms] = useState<any[]>([]);
  const [isLoadingSimilar, setIsLoadingSimilar] = useState(false);
  const [similarFilmStatuses, setSimilarFilmStatuses] = useState<{[kinopoiskId: string]: {existsInDb: boolean, filmData?: any}}>({});
  
  // Состояние для редактирования комментариев
  const [editingCommentId, setEditingCommentId] = useState<number | null>(null);
  const [editingContent, setEditingContent] = useState('');

  useEffect(() => {
    if (filmId) {
      fetchFilmDetails(filmId);
      fetchFilmComments(filmId);
      loadFilmStuff();
      loadFilmStills();
      loadRecommendedFilms();
      loadSimilarFilms();
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

  const loadRecommendedFilms = async () => {
    try {
      setIsLoadingRecommendations(true);
      const recommendations = await FilmsAPI.getFilmRecommendations(filmId, 10);
      setRecommendedFilms(recommendations.items);
    } catch (error) {
      console.error('Error loading film recommendations:', error);
    } finally {
      setIsLoadingRecommendations(false);
    }
  };

  const loadSimilarFilms = async () => {
    try {
      setIsLoadingSimilar(true);
      const similar = await FilmsAPI.getSimilarFilms(filmId);
      
      // Проверяем доступность каждого фильма в базе
      const filmStatuses: {[kinopoiskId: string]: {existsInDb: boolean, filmData?: any}} = {};
      
      for (const similarFilm of similar) {
        const kinopoiskId = similarFilm.similar_film_id;
        try {
          const filmData = await FilmsAPI.getFilmByKinopoiskId(kinopoiskId);
          filmStatuses[kinopoiskId] = { existsInDb: true, filmData };
        } catch (error) {
          // Фильм не найден в базе
          filmStatuses[kinopoiskId] = { existsInDb: false };
        }
      }
      
      setSimilarFilmStatuses(filmStatuses);
      setSimilarFilms(similar);
    } catch (error) {
      console.error('Error loading similar films:', error);
    } finally {
      setIsLoadingSimilar(false);
    }
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim() || !user) return;

    await addComment(filmId, newComment.trim());
    setNewComment('');
  };

  const handleEditComment = (commentId: number, content: string) => {
    setEditingCommentId(commentId);
    setEditingContent(content);
  };

  const handleSaveEdit = async (commentId: number) => {
    if (!editingContent.trim()) return;

    await updateComment(commentId, editingContent.trim());
    setEditingCommentId(null);
    setEditingContent('');
  };

  const handleCancelEdit = () => {
    setEditingCommentId(null);
    setEditingContent('');
  };

  const handleDeleteComment = async (commentId: number) => {
    if (confirm('Вы уверены, что хотите удалить этот комментарий?')) {
      await deleteComment(commentId);
    }
  };

  const handleBookmarkToggle = async () => {
    const isBookmarked = bookmarkedFilmIds.has(filmId);
    if (isBookmarked) {
      await removeBookmark(filmId);
    } else {
      await addBookmark(filmId);
    }
  };

  const canEditComment = (comment: any) => {
    return user && comment.user_id === user.id;
  };

  const isBookmarked = bookmarkedFilmIds.has(filmId);

  // Функция копирования URL
  const handleShare = async () => {
    const shareUrl = `${window.location.origin}/films/${filmId}`;
    await navigator.clipboard.writeText(shareUrl);
    toast.success('Ссылка скопирована в буфер обмена!');
  };

  if (isLoading || !currentFilm) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Skeleton className="h-8 w-48 mb-4" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <Skeleton className="aspect-2/3 w-full" />
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
    <div className="min-h-screen bg-linear-to-br from-background via-background to-muted/30">
      <div className="container mx-auto px-4 py-8 space-y-12">
        {/* Навигация */}
        <div className="mb-8">
          <Button asChild variant="ghost" className="text-muted-foreground hover:text-foreground">
            <Link href={ROUTES.FILMS}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              К списку фильмов
            </Link>
          </Button>
        </div>

        {/* Основная информация о фильме */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Постер */}
          <div className="lg:col-span-1">
            <Card className="p-0 top-8 overflow-hidden border-0 shadow-2xl">
              <CardContent className="p-0">
                {currentFilm.poster ? (
                  <div className="relative aspect-2/3 group">
                    <Image
                      src={currentFilm.poster}
                      alt={currentFilm.title || 'Без названия'}
                      fill
                      className="object-cover rounded-lg group-hover:scale-105 transition-transform duration-500 "
                      sizes="(max-width: 768px) 100vw, 33vw"
                      unoptimized={true}
                    />
                    <div className="absolute inset-0 bg-linear-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg" />
                    <div className="absolute bottom-4 left-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <Button className="w-full" size="lg">
                        <Play className="h-4 w-4 mr-2" />
                        Смотреть трейлер
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="aspect-2/3 bg-muted rounded-lg flex items-center justify-center">
                    <span className="text-muted-foreground">Нет постера</span>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Детали */}
          <div className="lg:col-span-2 space-y-8">
            {/* Заголовок */}
            <div className="space-y-4">
              <h1 className="text-4xl md:text-5xl font-bold bg-linear-to-r from-foreground to-foreground/80 bg-clip-text text-transparent">
                {currentFilm.title || currentFilm.original_title || 'Без названия'}
              </h1>
              {currentFilm.original_title && currentFilm.title !== currentFilm.original_title && (
                <p className="text-xl text-muted-foreground font-medium">
                  {currentFilm.original_title}
                </p>
              )}
              {currentFilm.tagline && (
                <p className="text-lg italic text-muted-foreground border-l-4 border-primary pl-4">
                  "{currentFilm.tagline}"
                </p>
              )}
            </div>

            {/* Кнопки действий */}
            <div className="flex flex-wrap gap-3">
              <StarRating
                filmId={filmId}
                interactive={true}
                size="lg"
              />
              {/* Кнопка закладок - только для авторизованных пользователей */}
              {isAuthenticated && (
                <Button
                  variant={isBookmarked ? "default" : "outline"}
                  onClick={handleBookmarkToggle}
                  disabled={isAddingBookmark}
                  className="shadow-lg"
                >
                  <Heart className={`h-4 w-4 mr-2 ${isBookmarked ? 'fill-current' : ''}`} />
                  {isBookmarked ? 'В закладках' : 'В закладки'}
                </Button>
              )}
              <Button variant="outline" className="shadow-lg" onClick={handleShare}>
                <Share className="h-4 w-4 mr-2" />
                Поделиться
              </Button>
              <Button variant="outline" className="shadow-lg">
                <Eye className="h-4 w-4 mr-2" />
                Смотреть
              </Button>
            </div>

            {/* Метаинформация */}
            <div className="flex flex-wrap gap-6 text-sm text-muted-foreground">
              {currentFilm.year && (
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-primary" />
                  <span className="font-medium">{currentFilm.year}</span>
                </div>
              )}
              {currentFilm.duration && (
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-primary" />
                  <span className="font-medium">{currentFilm.duration}</span>
                </div>
              )}
              {currentFilm.content_rating && (
                <Badge variant="secondary" className="font-medium">
                  {currentFilm.content_rating}
                </Badge>
              )}
            </div>

            {/* Рейтинги */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {currentFilm.rating_kp && (
                <Card className="border-primary/20 bg-linear-to-br from-primary/5 to-primary/10">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-primary/10 rounded-full">
                        <Star className="h-5 w-5 text-primary" />
                      </div>
                      <span className="font-semibold">Кинопоиск</span>
                    </div>
                    <p className="text-3xl font-bold text-primary">{currentFilm.rating_kp}</p>
                    <p className="text-sm text-muted-foreground">
                      {currentFilm.kp_votes_count} голосов
                    </p>
                  </CardContent>
                </Card>
              )}
              {currentFilm.rating_imdb && (
                <Card className="border-yellow-500/20 bg-linear-to-br from-yellow-500/5 to-yellow-500/10">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-yellow-500/10 rounded-full">
                        <Star className="h-5 w-5 text-yellow-500" />
                      </div>
                      <span className="font-semibold">IMDB</span>
                    </div>
                    <p className="text-3xl font-bold text-yellow-500">{currentFilm.rating_imdb}</p>
                    <p className="text-sm text-muted-foreground">
                      {currentFilm.imdb_votes_count} голосов
                    </p>
                  </CardContent>
                </Card>
              )}
              {currentFilm.user_rating && (
                <Card className="border-blue-500/20 bg-linear-to-br from-blue-500/5 to-blue-500/10">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 bg-blue-500/10 rounded-full">
                        <Users className="h-5 w-5 text-blue-500" />
                      </div>
                      <span className="font-semibold">Пользователи</span>
                    </div>
                    <p className="text-3xl font-bold text-blue-500">{currentFilm.user_rating}</p>
                    <p className="text-sm text-muted-foreground">
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
                  <h3 className="font-semibold mb-3 text-lg">Жанры</h3>
                  <div className="flex flex-wrap gap-2">
                    {currentFilm.genres.map((genre) => (
                      <Badge key={genre.id} variant="secondary" className="px-3 py-1">
                        {genre.name}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              {currentFilm.countries.length > 0 && (
                <div>
                  <h3 className="font-semibold mb-3 text-lg">Страны</h3>
                  <div className="flex flex-wrap gap-2">
                    {currentFilm.countries.map((country) => (
                      <Badge key={country.id} variant="outline" className="px-3 py-1">
                        <MapPin className="h-3 w-3 mr-1" />
                        {country.name}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Описание */}
        {(currentFilm.full_description || currentFilm.description) && (
          <section className="space-y-6">
            <Card className="border-0 shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl">Описание</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {currentFilm.full_description && (
                  <div>
                    <h4 className="font-semibold mb-3 text-lg">Полное описание</h4>
                    <p className="text-muted-foreground leading-relaxed text-lg">
                      {currentFilm.full_description}
                    </p>
                  </div>
                )}
                
                {currentFilm.description && (
                  <div>
                    <h4 className="font-semibold mb-3 text-lg">Краткое описание</h4>
                    <p className="text-muted-foreground leading-relaxed">
                      {currentFilm.description}
                    </p>
                  </div>
                )}

                {/* Дополнительная информация */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-6 border-t">
                  {currentFilm.budget && (
                    <div className="space-y-2">
                      <h5 className="font-semibold">Бюджет</h5>
                      <p className="text-muted-foreground">{currentFilm.budget}</p>
                    </div>
                  )}
                  {currentFilm.usa_box_office && (
                    <div className="space-y-2">
                      <h5 className="font-semibold">Сборы в США</h5>
                      <p className="text-muted-foreground">{currentFilm.usa_box_office}</p>
                    </div>
                  )}
                  {currentFilm.rus_box_office && (
                    <div className="space-y-2">
                      <h5 className="font-semibold">Сборы в России</h5>
                      <p className="text-muted-foreground">{currentFilm.rus_box_office}</p>
                    </div>
                  )}
                  {currentFilm.ru_premiere && (
                    <div className="space-y-2">
                      <h5 className="font-semibold">Премьера в России</h5>
                      <p className="text-muted-foreground">{currentFilm.ru_premiere}</p>
                    </div>
                  )}
                  {currentFilm.world_premiere && (
                    <div className="space-y-2">
                      <h5 className="font-semibold">Мировая премьера</h5>
                      <p className="text-muted-foreground">{currentFilm.world_premiere}</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </section>
        )}

        {/* Участники */}
        {filmStuff.length > 0 && (
          <section className="space-y-6">
            <Card className="border-0 shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl flex items-center gap-2">
                  <Users className="h-6 w-6" />
                  Участники
                </CardTitle>
              </CardHeader>
              <CardContent>
                {isLoadingStuff ? (
                  <div className="flex gap-4 overflow-hidden">
                    {Array.from({ length: 8 }).map((_, i) => (
                      <div key={i} className="shrink-0 w-80">
                        <Skeleton className="h-24 w-full" />
                      </div>
                    ))}
                  </div>
                ) : (
                  <ScrollArea className="w-full">
                    <div className="flex gap-4 pb-4">
                      {filmStuff.map((person) => (
                        <div key={person.id} className="shrink-0 w-80">
                          <MiniPersonCard person={person} />
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                )}
              </CardContent>
            </Card>
          </section>
        )}

        {/* Кадры из фильма */}
        {(filmStills.stills.length > 0 || filmStills.wall.length > 0) && (
          <section className="space-y-8">
            {/* Stills */}
            {filmStills.stills.length > 0 && (
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-2xl">Кадры из фильма</CardTitle>
                    <Button asChild variant="outline" size="sm">
                      <Link href={ROUTES.POSTERS(filmId)}>
                        <ImageIcon className="h-4 w-4 mr-2" />
                        Посмотреть все ({filmStills.stills.length})
                      </Link>
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  {isLoadingStills ? (
                    <div className="flex gap-4 overflow-hidden">
                      {Array.from({ length: 6 }).map((_, i) => (
                        <div key={i} className="shrink-0 w-80">
                          <StillCardSkeleton />
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex gap-4 overflow-x-auto pb-4">
                      {filmStills.stills.slice(0, 6).map((still) => (
                        <div key={still.id} className="shrink-0 w-80">
                          <StillCard still={still} />
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Wallpapers */}
            {filmStills.wall.length > 0 && (
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-2xl">Обои</CardTitle>
                    <Button asChild variant="outline" size="sm">
                      <Link href={ROUTES.POSTERS(filmId)}>
                        <ImageIcon className="h-4 w-4 mr-2" />
                        Посмотреть все ({filmStills.wall.length})
                      </Link>
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  {isLoadingStills ? (
                    <div className="flex gap-4 overflow-hidden">
                      {Array.from({ length: 6 }).map((_, i) => (
                        <div key={i} className="shrink-0 w-80">
                          <StillCardSkeleton />
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex gap-4 overflow-x-auto pb-4">
                      {filmStills.wall.slice(0, 6).map((wall) => (
                        <div key={wall.id} className="shrink-0 w-80">
                          <StillCard still={wall} />
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </section>
        )}

        {/* Рекомендуемые фильмы */}
        {recommendedFilms.length > 0 && (
          <section className="space-y-6">
            <Card className="border-0 shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl flex items-center gap-2">
                  <TrendingUp className="h-6 w-6" />
                  Рекомендуемые фильмы
                </CardTitle>
              </CardHeader>
              <CardContent>
                {isLoadingRecommendations ? (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {Array.from({ length: 12 }).map((_, i) => (
                      <FilmCardSkeleton key={i} />
                    ))}
                  </div>
                ) : (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {recommendedFilms.map((film) => (
                      <FilmCard key={film.id} film={film} />
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </section>
        )}

        {/* Похожие фильмы */}
        {similarFilms.length > 0 && (
          <section className="space-y-6">
            <Card className="border-0 shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl flex items-center gap-2">
                  <TrendingUp className="h-6 w-6" />
                  Похожие фильмы
                </CardTitle>
              </CardHeader>
              <CardContent>
                {isLoadingSimilar ? (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {Array.from({ length: 6 }).map((_, i) => (
                      <FilmCardSkeleton key={i} />
                    ))}
                  </div>
                ) : (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {similarFilms.map((film) => {
                      const kinopoiskId = film.similar_film_id;
                      const filmStatus = similarFilmStatuses[kinopoiskId];
                      
                      if (filmStatus?.existsInDb && filmStatus.filmData) {
                        // Фильм есть в базе - используем обычную ссылку
                        return (
                          <FilmCard
                              key={film.id}
                              film={{
                                id: filmStatus.filmData.id,
                                kinopoisk_id: filmStatus.filmData.kinopoisk_id,
                                title: filmStatus.filmData.title,
                                original_title: filmStatus.filmData.original_title,
                                poster: filmStatus.filmData.poster,
                                year: filmStatus.filmData.year,
                                rating_kp: filmStatus.filmData.rating_kp,
                                rating_imdb: filmStatus.filmData.rating_imdb,
                                description: filmStatus.filmData.description,
                                duration: filmStatus.filmData.duration,
                                user_rating: filmStatus.filmData.user_rating,
                                user_rating_count: filmStatus.filmData.user_rating_count,
                                is_family_friendly: filmStatus.filmData.is_family_friendly || false,
                              }}
                            />
                        );
                      } else {
                        // Фильма нет в базе - используем FilmCard с флагом isExternal
                        const externalUrl = `https://www.kinopoisk.ru/film/${kinopoiskId}/`;
                        return (
                          <FilmCard
                            key={film.id}
                            isExternal={true}
                            externalUrl={externalUrl}
                            showActions={false}
                            film={{
                              id: parseInt(kinopoiskId), // Используем kinopoisk_id как id для совместимости
                              kinopoisk_id: kinopoiskId,
                              title: film.similar_film_title,
                              poster: film.similar_film_poster,
                              year: film.similar_film_year ? parseInt(film.similar_film_year) : undefined,
                              rating_kp: film.similar_film_rating ? parseFloat(film.similar_film_rating) : undefined,
                              is_family_friendly: false, // Значение по умолчанию
                              user_rating_count: 0, // Значение по умолчанию
                            }}
                          />
                        );
                      }
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </section>
        )}

        {/* Комментарии */}
        <section className="space-y-6">
          <Card className="border-0 shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl flex items-center gap-2">
                <MessageSquare className="h-6 w-6" />
                Комментарии {comments.length > 0 && `(${comments.length})`}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Форма добавления комментария */}
              {user && (
                <form onSubmit={handleCommentSubmit} className="space-y-4">
                  <Textarea
                    placeholder="Напишите ваш комментарий..."
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    className="min-h-[120px] resize-none"
                    disabled={isAddingComment}
                  />
                  <Button 
                    type="submit" 
                    disabled={!newComment.trim() || isAddingComment}
                    className="shadow-lg"
                  >
                    <Send className="h-4 w-4 mr-2" />
                    {isAddingComment ? 'Отправка...' : 'Отправить комментарий'}
                  </Button>
                </form>
              )}

              {!user && (
                <div className="text-center py-8">
                  <p className="text-muted-foreground mb-4">
                    Войдите в аккаунт, чтобы оставлять комментарии
                  </p>
                  <Button asChild variant="outline">
                    <Link href={ROUTES.LOGIN}>Войти</Link>
                  </Button>
                </div>
              )}

              <Separator />

              {/* Список комментариев */}
              {isLoadingComments ? (
                <div className="space-y-4">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <div key={i} className="space-y-3">
                      <Skeleton className="h-4 w-1/3" />
                      <Skeleton className="h-20 w-full" />
                      <Skeleton className="h-3 w-1/4" />
                    </div>
                  ))}
                </div>
              ) : comments.length > 0 ? (
                <div className="space-y-4">
                  {comments.map((comment) => (
                    <div key={comment.id} className="border rounded-lg p-6 bg-card/50 hover:bg-card/80 transition-colors">
                      <div className="flex items-start justify-between mb-4">
                        <div className="space-y-1">
                          <span className="font-semibold">
                            {/* Доступ к пользователю через поле user_id */}
                            <span>Пользователь #{comment.user_id}</span>
                          </span>
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <span>{new Date(comment.created_at).toLocaleDateString('ru-RU')}</span>
                            {comment.is_edited && (
                              <span className="text-xs">(изменено)</span>
                            )}
                          </div>
                        </div>
                        {canEditComment(comment) && !comment.is_deleted && (
                          <div className="flex gap-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleEditComment(comment.id, comment.content)}
                              disabled={editingCommentId === comment.id}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleDeleteComment(comment.id)}
                              disabled={isAddingComment}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        )}
                      </div>
                      
                      {comment.is_deleted ? (
                        <p className="text-muted-foreground italic">
                          [Комментарий удален]
                        </p>
                      ) : editingCommentId === comment.id ? (
                        <div className="space-y-3">
                          <Textarea
                            value={editingContent}
                            onChange={(e) => setEditingContent(e.target.value)}
                            className="min-h-[100px] resize-none"
                            placeholder="Редактируйте ваш комментарий..."
                          />
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              onClick={() => handleSaveEdit(comment.id)}
                              disabled={!editingContent.trim() || isAddingComment}
                            >
                              Сохранить
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={handleCancelEdit}
                              disabled={isAddingComment}
                            >
                              Отмена
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <p className="text-foreground leading-relaxed">{comment.content}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <MessageSquare className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <p className="text-muted-foreground text-lg mb-2">
                    Комментариев пока нет
                  </p>
                  <p className="text-muted-foreground">
                    Будьте первым, кто оставит отзыв!
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  );
}