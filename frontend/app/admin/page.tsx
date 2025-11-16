'use client';

import { useState, useEffect } from 'react';
import { AdminAPI } from '@/lib/api';
import { FilmWithDetails, Stuff } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Edit, 
  Trash2, 
  Plus, 
  Film, 
  Users, 
  Star, 
  Calendar, 
  Clock,
} from 'lucide-react';
import StuffForm from '@/components/admin/StuffForm';
import FilmForm from '@/components/admin/FilmForm';

interface FilmsResponse extends Array<FilmWithDetails> {}
interface StuffResponse {
  items: Stuff[];
  page: number;
  page_size: number;
  total_count: number;
}

export default function AdminPage() {
  const [films, setFilms] = useState<FilmsResponse | null>(null);
  const [stuff, setStuff] = useState<StuffResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [editingFilm, setEditingFilm] = useState<FilmWithDetails | null>(null);
  const [editingStuff, setEditingStuff] = useState<Stuff | null>(null);
  const [showFilmDialog, setShowFilmDialog] = useState(false);
  const [showStuffDialog, setShowStuffDialog] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const showMessage = (msg: string) => {
    setMessage(msg);
    setTimeout(() => setMessage(''), 3000);
  };

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [filmsData, stuffData] = await Promise.all([
        AdminAPI.getAllFilms(1, 100),
        AdminAPI.getAllStuff(1, 100)
      ]) as [FilmsResponse, StuffResponse];
      
      setFilms(filmsData);
      setStuff(stuffData);
    } catch (error) {
      console.error('Error loading data:', error);
      showMessage('Ошибка загрузки данных');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilmSubmit = async (filmData: any) => {
    try {
      if (editingFilm) {
        await AdminAPI.updateFilm(editingFilm.id, filmData);
        showMessage('Фильм обновлен');
      } else {
        await AdminAPI.createFilm(filmData);
        showMessage('Фильм создан');
      }
      setShowFilmDialog(false);
      setEditingFilm(null);
      loadData();
    } catch (error) {
      console.error('Error saving film:', error);
      showMessage('Ошибка сохранения фильма');
    }
  };

  const handleStuffSubmit = async (stuffData: any) => {
    try {
      if (editingStuff) {
        await AdminAPI.updateStuff(editingStuff.id, stuffData);
        showMessage('Участник обновлен');
      } else {
        await AdminAPI.createStuff(stuffData);
        showMessage('Участник создан');
      }
      setShowStuffDialog(false);
      setEditingStuff(null);
      loadData();
    } catch (error) {
      console.error('Error saving stuff:', error);
      showMessage('Ошибка сохранения участника');
    }
  };

  const handleDeleteFilm = async (filmId: number) => {
    try {
      await AdminAPI.deleteFilm(filmId);
      showMessage('Фильм удален');
      loadData();
    } catch (error) {
      console.error('Error deleting film:', error);
      showMessage('Ошибка удаления фильма');
    }
  };

  const handleDeleteStuff = async (stuffId: number) => {
    try {
      await AdminAPI.deleteStuff(stuffId);
      showMessage('Участник удален');
      loadData();
    } catch (error) {
      console.error('Error deleting stuff:', error);
      showMessage('Ошибка удаления участника');
    }
  };

  const formatArrayField = (field: string[] | null | undefined) => {
    if (!field || field.length === 0) return '-';
    return field.join(', ');
  };

  const formatRating = (rating: number | null | undefined) => {
    return rating ? rating.toFixed(1) : '-';
  };

  const formatYear = (year: number | null | undefined) => {
    return year || '-';
  };

  const formatDuration = (duration: string | null | undefined) => {
    return duration || '-';
  };

  const formatBoxOffice = (amount: string | null | undefined) => {
    return amount || '-';
  };

  if (isLoading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Загрузка данных...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Админ панель</h1>
          <p className="text-muted-foreground">
            Управление фильмами и участниками
          </p>
        </div>
      </div>
      
      {message && (
        <Card className="border-green-200 bg-green-50">
          <CardContent className="p-4">
            <p className="text-green-800">{message}</p>
          </CardContent>
        </Card>
      )}
      
      <Tabs defaultValue="films" className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="films" className="flex items-center gap-2">
            <Film className="h-4 w-4" />
            Фильмы ({films?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="stuff" className="flex items-center gap-2">
            <Users className="h-4 w-4" />
            Участники ({stuff?.total_count || 0})
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="films" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Film className="h-5 w-5" />
                  Управление фильмами
                </CardTitle>
                <Dialog open={showFilmDialog} onOpenChange={setShowFilmDialog}>
                  <DialogTrigger asChild>
                    <Button onClick={() => setEditingFilm(null)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Добавить фильм
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-4xl max-h-[90vh]">
                    <DialogHeader>
                      <DialogTitle>
                        {editingFilm ? 'Редактировать фильм' : 'Добавить фильм'}
                      </DialogTitle>
                    </DialogHeader>
                    <ScrollArea className="max-h-[70vh] pr-4">
                      <FilmForm
                        film={editingFilm}
                        onSubmit={handleFilmSubmit}
                        onCancel={() => setShowFilmDialog(false)}
                      />
                    </ScrollArea>
                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[600px]">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>kpID</TableHead>
                      <TableHead>Название</TableHead>
                      <TableHead>Оригинальное название</TableHead>
                      <TableHead>Год</TableHead>
                      <TableHead>Жанры</TableHead>
                      <TableHead>Страны</TableHead>
                      <TableHead>Рейтинг КП</TableHead>
                      <TableHead>Рейтинг IMDb</TableHead>
                      <TableHead>Длительность</TableHead>
                      <TableHead>Премьера</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {films?.map((film: FilmWithDetails) => (
                      <TableRow key={film.id}>
                        <TableCell className="font-mono text-sm">
                          {film.id}
                        </TableCell>
                        <TableCell className="font-mono text-sm">
                          {film.kinopoisk_id}
                        </TableCell>
                        <TableCell className="font-medium max-w-[200px]">
                          <div className="truncate" title={film.title || ''}>
                            {film.title || '-'}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[200px]">
                          <div className="truncate" title={film.original_title || ''}>
                            {film.original_title || '-'}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="secondary">
                            {formatYear(film.year)}
                          </Badge>
                        </TableCell>
                        <TableCell className="max-w-[150px]">
                          <div className="flex flex-wrap gap-1">
                            {film.genres?.slice(0, 2).map((genre: { id: number; name: string }) => (
                              <Badge key={genre.id} variant="outline" className="text-xs">
                                {genre.name}
                              </Badge>
                            ))}
                            {film.genres && film.genres.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{film.genres.length - 2}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[120px]">
                          <div className="flex flex-wrap gap-1">
                            {film.countries?.slice(0, 2).map((country: { id: number; name: string }) => (
                              <Badge key={country.id} variant="outline" className="text-xs">
                                {country.name}
                              </Badge>
                            ))}
                            {film.countries && film.countries.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{film.countries.length - 2}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Star className="h-3 w-3 text-yellow-500" />
                            {formatRating(film.rating_kp)}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Star className="h-3 w-3 text-blue-500" />
                            {formatRating(film.rating_imdb)}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3 text-gray-500" />
                            {formatDuration(film.duration)}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Calendar className="h-3 w-3 text-gray-500" />
                            {film.ru_premiere || '-'}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setEditingFilm(film);
                                setShowFilmDialog(true);
                              }}
                            >
                              <Edit className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDeleteFilm(film.id)}
                            >
                              <Trash2 className="h-3 w-3" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="stuff" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Управление участниками
                </CardTitle>
                <Dialog open={showStuffDialog} onOpenChange={setShowStuffDialog}>
                  <DialogTrigger asChild>
                    <Button onClick={() => setEditingStuff(null)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Добавить участника
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-4xl max-h-[90vh]">
                    <DialogHeader>
                      <DialogTitle>
                        {editingStuff ? 'Редактировать участника' : 'Добавить участника'}
                      </DialogTitle>
                    </DialogHeader>
                    <ScrollArea className="max-h-[70vh] pr-4">
                      <StuffForm
                        stuff={editingStuff}
                        onSubmit={handleStuffSubmit}
                        onCancel={() => setShowStuffDialog(false)}
                      />
                    </ScrollArea>
                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[600px]">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>kpID</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead>Оригинальное имя</TableHead>
                      <TableHead>Карьера</TableHead>
                      <TableHead>Жанры</TableHead>
                      <TableHead>Возраст</TableHead>
                      <TableHead>Год рождения</TableHead>
                      <TableHead>Место рождения</TableHead>
                      <TableHead>Фильмов</TableHead>
                      <TableHead>Рост</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {stuff?.items?.map((person: Stuff) => (
                      <TableRow key={person.id}>
                        <TableCell className="font-mono text-sm">
                          {person.id}
                        </TableCell>
                        <TableCell className="font-mono text-sm">
                          {person.kinopoisk_id}
                        </TableCell>
                        <TableCell className="font-medium max-w-[150px]">
                          <div className="truncate" title={person.name || ''}>
                            {person.name || '-'}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[150px]">
                          <div className="truncate" title={person.original_name || ''}>
                            {person.original_name || '-'}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[120px]">
                          <div className="flex flex-wrap gap-1">
                            {person.career?.slice(0, 2).map((career: string, index: number) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {career}
                              </Badge>
                            ))}
                            {person.career && person.career.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{person.career.length - 2}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[100px]">
                          <div className="flex flex-wrap gap-1">
                            {person.ganres?.slice(0, 2).map((genre: string, index: number) => (
                              <Badge key={index} variant="secondary" className="text-xs">
                                {genre}
                              </Badge>
                            ))}
                            {person.ganres && person.ganres.length > 2 && (
                              <Badge variant="secondary" className="text-xs">
                                +{person.ganres.length - 2}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">
                            {person.age || '-'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Calendar className="h-3 w-3 text-gray-500" />
                            {person.birthday_day_month || '-'}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[100px]">
                          <div className="truncate" title={formatArrayField(person.birthplace)}>
                            {formatArrayField(person.birthplace)}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Film className="h-3 w-3 text-gray-500" />
                            {person.total_films || '-'}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">
                            {person.height || '-'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setEditingStuff(person);
                                setShowStuffDialog(true);
                              }}
                            >
                              <Edit className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDeleteStuff(person.id)}
                            >
                              <Trash2 className="h-3 w-3" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
