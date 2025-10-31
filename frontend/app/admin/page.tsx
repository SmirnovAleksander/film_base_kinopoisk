'use client';

import { useState, useEffect } from 'react';
import { AdminAPI } from '@/lib/api';
import { FilmWithDetails, Stuff } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { 
  Edit, 
  Trash2, 
  Plus, 
  Film, 
  Users, 
  Star, 
  Calendar, 
  Globe, 
  Clock,
  DollarSign,
  Eye,
  Heart
} from 'lucide-react';

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

function FilmForm({ film, onSubmit, onCancel }: any) {
  const [formData, setFormData] = useState({
    kinopoisk_id: film?.kinopoisk_id || '',
    title: film?.title || '',
    original_title: film?.original_title || '',
    description: film?.description || '',
    full_description: film?.full_description || '',
    year: film?.year?.toString() || '',
    tagline: film?.tagline || '',
    poster: film?.poster || '',
    duration: film?.duration || '',
    rating_kp: film?.rating_kp?.toString() || '',
    rating_imdb: film?.rating_imdb?.toString() || '',
    budget: film?.budget || '',
    rus_box_office: film?.rus_box_office || '',
    usa_box_office: film?.usa_box_office || '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const submitData = {
      ...formData,
      year: formData.year ? parseInt(formData.year) : null,
      rating_kp: formData.rating_kp ? parseFloat(formData.rating_kp) : null,
      rating_imdb: formData.rating_imdb ? parseFloat(formData.rating_imdb) : null,
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="kinopoisk_id">Kinopoisk ID</Label>
          <Input
            id="kinopoisk_id"
            value={formData.kinopoisk_id}
            onChange={(e) => setFormData({ ...formData, kinopoisk_id: e.target.value })}
            required
          />
        </div>
        <div>
          <Label htmlFor="year">Год</Label>
          <Input
            id="year"
            type="number"
            value={formData.year}
            onChange={(e) => setFormData({ ...formData, year: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="title">Название</Label>
          <Input
            id="title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="original_title">Оригинальное название</Label>
          <Input
            id="original_title"
            value={formData.original_title}
            onChange={(e) => setFormData({ ...formData, original_title: e.target.value })}
          />
        </div>
      </div>

      <div>
        <Label htmlFor="tagline">Слоган</Label>
        <Input
          id="tagline"
          value={formData.tagline}
          onChange={(e) => setFormData({ ...formData, tagline: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="description">Краткое описание</Label>
        <Textarea
          id="description"
          rows={3}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="full_description">Полное описание</Label>
        <Textarea
          id="full_description"
          rows={5}
          value={formData.full_description}
          onChange={(e) => setFormData({ ...formData, full_description: e.target.value })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="duration">Длительность</Label>
          <Input
            id="duration"
            placeholder="120 мин"
            value={formData.duration}
            onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="poster">Ссылка на постер</Label>
          <Input
            id="poster"
            value={formData.poster}
            onChange={(e) => setFormData({ ...formData, poster: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="rating_kp">Рейтинг Кинопоиска</Label>
          <Input
            id="rating_kp"
            type="number"
            step="0.1"
            min="0"
            max="10"
            value={formData.rating_kp}
            onChange={(e) => setFormData({ ...formData, rating_kp: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="rating_imdb">Рейтинг IMDb</Label>
          <Input
            id="rating_imdb"
            type="number"
            step="0.1"
            min="0"
            max="10"
            value={formData.rating_imdb}
            onChange={(e) => setFormData({ ...formData, rating_imdb: e.target.value })}
          />
        </div>
      </div>

      <div className="space-y-4">
        <Label>Кассовые сборы</Label>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <Label htmlFor="budget">Бюджет</Label>
            <Input
              id="budget"
              placeholder="$50,000,000"
              value={formData.budget}
              onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
            />
          </div>
          <div>
            <Label htmlFor="usa_box_office">Сборы в США</Label>
            <Input
              id="usa_box_office"
              placeholder="$100,000,000"
              value={formData.usa_box_office}
              onChange={(e) => setFormData({ ...formData, usa_box_office: e.target.value })}
            />
          </div>
          <div>
            <Label htmlFor="rus_box_office">Сборы в России</Label>
            <Input
              id="rus_box_office"
              placeholder="₽500,000,000"
              value={formData.rus_box_office}
              onChange={(e) => setFormData({ ...formData, rus_box_office: e.target.value })}
            />
          </div>
        </div>
      </div>

      <Separator />

      <div className="flex space-x-2">
        <Button type="submit">Сохранить</Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
      </div>
    </form>
  );
}

function StuffForm({ stuff, onSubmit, onCancel }: any) {
  const [formData, setFormData] = useState({
    kinopoisk_id: stuff?.kinopoisk_id || '',
    name: stuff?.name || '',
    original_name: stuff?.original_name || '',
    career: stuff?.career?.join(', ') || '',
    ganres: stuff?.ganres?.join(', ') || '',
    height: stuff?.height || '',
    birthday_day_month: stuff?.birthday_day_month || '',
    zodiac: stuff?.zodiac || '',
    age: stuff?.age?.toString() || '',
    birthplace: stuff?.birthplace?.join(', ') || '',
    spouse: stuff?.spouse?.join(', ') || '',
    children: stuff?.children?.join(', ') || '',
    total_films: stuff?.total_films?.toString() || '',
    career_start_year: stuff?.career_start_year?.toString() || '',
    career_end_year: stuff?.career_end_year?.toString() || '',
    image: stuff?.image || '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const submitData = {
      ...formData,
      age: formData.age ? parseInt(formData.age) : null,
      total_films: formData.total_films ? parseInt(formData.total_films) : null,
      career_start_year: formData.career_start_year ? parseInt(formData.career_start_year) : null,
      career_end_year: formData.career_end_year ? parseInt(formData.career_end_year) : null,
      career: formData.career.split(',').map((s: string) => s.trim()).filter(Boolean),
      ganres: formData.ganres.split(',').map((s: string) => s.trim()).filter(Boolean),
      birthplace: formData.birthplace.split(',').map((s: string) => s.trim()).filter(Boolean),
      spouse: formData.spouse.split(',').map((s: string) => s.trim()).filter(Boolean),
      children: formData.children.split(',').map((s: string) => s.trim()).filter(Boolean),
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="kinopoisk_id">Kinopoisk ID</Label>
          <Input
            id="kinopoisk_id"
            value={formData.kinopoisk_id}
            onChange={(e) => setFormData({ ...formData, kinopoisk_id: e.target.value })}
            required
          />
        </div>
        <div>
          <Label htmlFor="age">Возраст</Label>
          <Input
            id="age"
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="name">Имя</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="original_name">Оригинальное имя</Label>
          <Input
            id="original_name"
            value={formData.original_name}
            onChange={(e) => setFormData({ ...formData, original_name: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="height">Рост</Label>
          <Input
            id="height"
            placeholder="180 см"
            value={formData.height}
            onChange={(e) => setFormData({ ...formData, height: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="zodiac">Знак зодиака</Label>
          <Input
            id="zodiac"
            value={formData.zodiac}
            onChange={(e) => setFormData({ ...formData, zodiac: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="birthday_day_month">День рождения</Label>
          <Input
            id="birthday_day_month"
            placeholder="15 июня"
            value={formData.birthday_day_month}
            onChange={(e) => setFormData({ ...formData, birthday_day_month: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="total_films">Количество фильмов</Label>
          <Input
            id="total_films"
            type="number"
            value={formData.total_films}
            onChange={(e) => setFormData({ ...formData, total_films: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="career_start_year">Начало карьеры</Label>
          <Input
            id="career_start_year"
            type="number"
            value={formData.career_start_year}
            onChange={(e) => setFormData({ ...formData, career_start_year: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="career_end_year">Конец карьеры</Label>
          <Input
            id="career_end_year"
            type="number"
            value={formData.career_end_year}
            onChange={(e) => setFormData({ ...formData, career_end_year: e.target.value })}
          />
        </div>
      </div>

      <div>
        <Label htmlFor="career">Карьера (через запятую)</Label>
        <Input
          id="career"
          placeholder="Актер, Режиссер, Продюсер"
          value={formData.career}
          onChange={(e) => setFormData({ ...formData, career: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="ganres">Жанры (через запятую)</Label>
        <Input
          id="ganres"
          placeholder="Драма, Комедия, Боевик"
          value={formData.ganres}
          onChange={(e) => setFormData({ ...formData, ganres: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="birthplace">Место рождения (через запятую)</Label>
        <Input
          id="birthplace"
          placeholder="Москва, Россия"
          value={formData.birthplace}
          onChange={(e) => setFormData({ ...formData, birthplace: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="spouse">Супруг(а) (через запятую)</Label>
        <Input
          id="spouse"
          placeholder="Имя супруги"
          value={formData.spouse}
          onChange={(e) => setFormData({ ...formData, spouse: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="children">Дети (через запятую)</Label>
        <Input
          id="children"
          placeholder="Имена детей"
          value={formData.children}
          onChange={(e) => setFormData({ ...formData, children: e.target.value })}
        />
      </div>

      <div>
        <Label htmlFor="image">Ссылка на фото</Label>
        <Input
          id="image"
          value={formData.image}
          onChange={(e) => setFormData({ ...formData, image: e.target.value })}
        />
      </div>

      <Separator />

      <div className="flex space-x-2">
        <Button type="submit">Сохранить</Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
      </div>
    </form>
  );
}