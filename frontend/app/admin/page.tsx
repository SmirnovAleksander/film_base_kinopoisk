'use client';

import { useState, useEffect } from 'react';
import { AdminAPI } from '@/lib/api';
import { FilmWithDetails, Stuff, Genre, Country, Media, User } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
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
  Tag,
  Globe,
  Newspaper,
  UserCog,
} from 'lucide-react';
import StuffForm from '@/components/admin/StuffForm';
import FilmForm from '@/components/admin/FilmForm';
import GenreForm from '@/components/admin/GenreForm';
import CountryForm from '@/components/admin/CountryForm';
import MediaForm from '@/components/admin/MediaForm';
import UserForm from '@/components/admin/UserForm';
import { AdminSidebar } from '@/components/admin/admin-sidebar';
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar';

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
  const [genres, setGenres] = useState<Genre[] | null>(null);
  const [countries, setCountries] = useState<Country[] | null>(null);
  const [media, setMedia] = useState<Media[] | null>(null);
  const [users, setUsers] = useState<User[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>('#films');
  const [editingFilm, setEditingFilm] = useState<FilmWithDetails | null>(null);
  const [editingStuff, setEditingStuff] = useState<Stuff | null>(null);
  const [editingGenre, setEditingGenre] = useState<Genre | null>(null);
  const [editingCountry, setEditingCountry] = useState<Country | null>(null);
  const [editingMedia, setEditingMedia] = useState<Media | null>(null);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [showFilmDialog, setShowFilmDialog] = useState(false);
  const [showStuffDialog, setShowStuffDialog] = useState(false);
  const [showGenreDialog, setShowGenreDialog] = useState(false);
  const [showCountryDialog, setShowCountryDialog] = useState(false);
  const [showMediaDialog, setShowMediaDialog] = useState(false);
  const [showUserDialog, setShowUserDialog] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash || '#films';
      setActiveTab(hash);
    };
    
    handleHashChange();
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

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
      const [filmsData, stuffData, genresData, countriesData, mediaData, usersData] = await Promise.all([
        AdminAPI.getAllFilms(1, 100),
        AdminAPI.getAllStuff(1, 100),
        AdminAPI.getAllGenres(),
        AdminAPI.getAllCountries(),
        AdminAPI.getAllMedia(1, 100),
        AdminAPI.getAllUsers(1, 100)
      ]) as [FilmsResponse, StuffResponse, Genre[], Country[], Media[], User[]];
      
      setFilms(filmsData);
      setStuff(stuffData);
      setGenres(genresData);
      setCountries(countriesData);
      setMedia(mediaData);
      setUsers(usersData);
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

  const handleGenreSubmit = async (genreData: any) => {
    try {
      if (editingGenre) {
        await AdminAPI.updateGenre(editingGenre.id, genreData);
        showMessage('Жанр обновлен');
      } else {
        await AdminAPI.createGenre(genreData);
        showMessage('Жанр создан');
      }
      setShowGenreDialog(false);
      setEditingGenre(null);
      loadData();
    } catch (error) {
      console.error('Error saving genre:', error);
      showMessage('Ошибка сохранения жанра');
    }
  };

  const handleCountrySubmit = async (countryData: any) => {
    try {
      if (editingCountry) {
        await AdminAPI.updateCountry(editingCountry.id, countryData);
        showMessage('Страна обновлена');
      } else {
        await AdminAPI.createCountry(countryData);
        showMessage('Страна создана');
      }
      setShowCountryDialog(false);
      setEditingCountry(null);
      loadData();
    } catch (error) {
      console.error('Error saving country:', error);
      showMessage('Ошибка сохранения страны');
    }
  };

  const handleDeleteGenre = async (genreId: number) => {
    try {
      await AdminAPI.deleteGenre(genreId);
      showMessage('Жанр удален');
      loadData();
    } catch (error) {
      console.error('Error deleting genre:', error);
      showMessage('Ошибка удаления жанра');
    }
  };

  const handleDeleteCountry = async (countryId: number) => {
    try {
      await AdminAPI.deleteCountry(countryId);
      showMessage('Страна удалена');
      loadData();
    } catch (error) {
      console.error('Error deleting country:', error);
      showMessage('Ошибка удаления страны');
    }
  };

  const handleMediaSubmit = async (mediaData: any) => {
    try {
      if (editingMedia) {
        await AdminAPI.updateMedia(editingMedia.id, mediaData);
        showMessage('Медиа обновлено');
      } else {
        await AdminAPI.createMedia(mediaData);
        showMessage('Медиа создано');
      }
      setShowMediaDialog(false);
      setEditingMedia(null);
      loadData();
    } catch (error) {
      console.error('Error saving media:', error);
      showMessage('Ошибка сохранения медиа');
    }
  };

  const handleDeleteMedia = async (mediaId: number) => {
    try {
      await AdminAPI.deleteMedia(mediaId);
      showMessage('Медиа удалено');
      loadData();
    } catch (error) {
      console.error('Error deleting media:', error);
      showMessage('Ошибка удаления медиа');
    }
  };

  const handleUserSubmit = async (userData: any) => {
    try {
      if (editingUser) {
        await AdminAPI.updateUser(editingUser.id, userData);
        showMessage('Пользователь обновлен');
      } else {
        await AdminAPI.createUser(userData);
        showMessage('Пользователь создан');
      }
      setShowUserDialog(false);
      setEditingUser(null);
      loadData();
    } catch (error) {
      console.error('Error saving user:', error);
      showMessage('Ошибка сохранения пользователя');
    }
  };

  const handleDeleteUser = async (userId: number) => {
    try {
      await AdminAPI.deleteUser(userId);
      showMessage('Пользователь удален');
      loadData();
    } catch (error) {
      console.error('Error deleting user:', error);
      showMessage('Ошибка удаления пользователя');
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

  const renderContent = () => {
    switch (activeTab) {
      case '#films':
        return renderFilmsContent();
      case '#stuff':
        return renderStuffContent();
      case '#genres':
        return renderGenresContent();
      case '#countries':
        return renderCountriesContent();
      case '#media':
        return renderMediaContent();
      case '#users':
        return renderUsersContent();
      default:
        return renderFilmsContent();
    }
  };

  if (isLoading) {
    return (
      <SidebarProvider>
        <AdminSidebar activeTab={activeTab} />
        <SidebarInset>
          <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Загрузка данных...</p>
          </div>
        </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  const renderFilmsContent = () => (
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
  );
        
  const renderStuffContent = () => (
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
  );

  const renderGenresContent = () => (
    <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Tag className="h-5 w-5" />
                  Управление жанрами
                </CardTitle>
                <Dialog open={showGenreDialog} onOpenChange={setShowGenreDialog}>
                  <DialogTrigger asChild>
                    <Button onClick={() => setEditingGenre(null)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Добавить жанр
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl">
                    <DialogHeader>
                      <DialogTitle>
                        {editingGenre ? 'Редактировать жанр' : 'Добавить жанр'}
                      </DialogTitle>
                    </DialogHeader>
                    <ScrollArea className="max-h-[70vh] pr-4">
                      <GenreForm
                        genre={editingGenre}
                        onSubmit={handleGenreSubmit}
                        onCancel={() => setShowGenreDialog(false)}
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
                      <TableHead>Название</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {genres?.map((genre: Genre) => (
                      <TableRow key={genre.id}>
                        <TableCell className="font-mono text-sm">
                          {genre.id}
                        </TableCell>
                        <TableCell className="font-medium">
                          <Badge variant="outline" className="text-sm">
                            {genre.name}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setEditingGenre(genre);
                                setShowGenreDialog(true);
                              }}
                            >
                              <Edit className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDeleteGenre(genre.id)}
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
  );

  const renderCountriesContent = () => (
    <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5" />
                  Управление странами
                </CardTitle>
                <Dialog open={showCountryDialog} onOpenChange={setShowCountryDialog}>
                  <DialogTrigger asChild>
                    <Button onClick={() => setEditingCountry(null)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Добавить страну
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl">
                    <DialogHeader>
                      <DialogTitle>
                        {editingCountry ? 'Редактировать страну' : 'Добавить страну'}
                      </DialogTitle>
                    </DialogHeader>
                    <ScrollArea className="max-h-[70vh] pr-4">
                      <CountryForm
                        country={editingCountry}
                        onSubmit={handleCountrySubmit}
                        onCancel={() => setShowCountryDialog(false)}
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
                      <TableHead>Название</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {countries?.map((country: Country) => (
                      <TableRow key={country.id}>
                        <TableCell className="font-mono text-sm">
                          {country.id}
                        </TableCell>
                        <TableCell className="font-medium">
                          <Badge variant="outline" className="text-sm">
                            {country.name}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setEditingCountry(country);
                                setShowCountryDialog(true);
                              }}
                            >
                              <Edit className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDeleteCountry(country.id)}
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
  );

  const renderMediaContent = () => (
    <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Newspaper className="h-5 w-5" />
                  Управление медиа
                </CardTitle>
                <Dialog open={showMediaDialog} onOpenChange={setShowMediaDialog}>
                  <DialogTrigger asChild>
                    <Button onClick={() => setEditingMedia(null)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Добавить медиа
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-4xl max-h-[90vh]">
                    <DialogHeader>
                      <DialogTitle>
                        {editingMedia ? 'Редактировать медиа' : 'Добавить медиа'}
                      </DialogTitle>
                    </DialogHeader>
                    <ScrollArea className="max-h-[70vh] pr-4">
                      <MediaForm
                        media={editingMedia}
                        onSubmit={handleMediaSubmit}
                        onCancel={() => setShowMediaDialog(false)}
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
                      <TableHead>Тип</TableHead>
                      <TableHead>Заголовок</TableHead>
                      <TableHead>Категория</TableHead>
                      <TableHead>Тип карточки</TableHead>
                      <TableHead>Дата</TableHead>
                      <TableHead>URL</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {media?.map((item: Media) => (
                      <TableRow key={item.id}>
                        <TableCell className="font-mono text-sm">
                          {item.id}
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">
                            {item.type || '-'}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-medium max-w-[200px]">
                          <div className="truncate" title={item.title || ''}>
                            {item.title || '-'}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="secondary">
                            {item.category || '-'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {item.card_type || '-'}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Calendar className="h-3 w-3 text-gray-500" />
                            {item.date || '-'}
                          </div>
                        </TableCell>
                        <TableCell className="max-w-[150px]">
                          <div className="truncate" title={item.url || ''}>
                            {item.url ? (
                              <a 
                                href={item.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline"
                              >
                                {item.url}
                              </a>
                            ) : '-'}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setEditingMedia(item);
                                setShowMediaDialog(true);
                              }}
                            >
                              <Edit className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDeleteMedia(item.id)}
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
  );

  const renderUsersContent = () => (
    <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <UserCog className="h-5 w-5" />
                  Управление пользователями
                </CardTitle>
                <Dialog open={showUserDialog} onOpenChange={setShowUserDialog}>
                  <DialogTrigger asChild>
                    <Button onClick={() => setEditingUser(null)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Добавить пользователя
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl max-h-[90vh]">
                    <DialogHeader>
                      <DialogTitle>
                        {editingUser ? 'Редактировать пользователя' : 'Добавить пользователя'}
                      </DialogTitle>
                    </DialogHeader>
                    <ScrollArea className="max-h-[70vh] pr-4">
                      <UserForm
                        user={editingUser}
                        onSubmit={handleUserSubmit}
                        onCancel={() => setShowUserDialog(false)}
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
                      <TableHead>Email</TableHead>
                      <TableHead>Имя пользователя</TableHead>
                      <TableHead>Имя</TableHead>
                      <TableHead>Фамилия</TableHead>
                      <TableHead>Активен</TableHead>
                      <TableHead>Суперпользователь</TableHead>
                      <TableHead>Подтвержден</TableHead>
                      <TableHead>Дата создания</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users?.map((user: User) => (
                      <TableRow key={user.id}>
                        <TableCell className="font-mono text-sm">
                          {user.id}
                        </TableCell>
                        <TableCell className="font-medium">
                          {user.email}
                        </TableCell>
                        <TableCell>
                          {user.username}
                        </TableCell>
                        <TableCell>
                          {user.first_name || '-'}
                        </TableCell>
                        <TableCell>
                          {user.last_name || '-'}
                        </TableCell>
                        <TableCell>
                          <Badge variant={user.is_active ? "default" : "secondary"}>
                            {user.is_active ? 'Да' : 'Нет'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={user.is_superuser ? "destructive" : "outline"}>
                            {user.is_superuser ? 'Да' : 'Нет'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={user.is_verified ? "default" : "secondary"}>
                            {user.is_verified ? 'Да' : 'Нет'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Calendar className="h-3 w-3 text-gray-500" />
                            {new Date(user.created_at).toLocaleDateString('ru-RU')}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-1">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setEditingUser(user);
                                setShowUserDialog(true);
                              }}
                            >
                              <Edit className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => handleDeleteUser(user.id)}
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
  );

  return (
    <SidebarProvider>
      <AdminSidebar 
        activeTab={activeTab}
        counts={{
          films: films?.length,
          stuff: stuff?.total_count,
          genres: genres?.length,
          countries: countries?.length,
          media: media?.length,
          users: users?.length,
        }}
      />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-semibold">Админ панель</h1>
          </div>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          {message && (
            <Card className="border-green-200 bg-green-50">
              <CardContent className="p-4">
                <p className="text-green-800">{message}</p>
              </CardContent>
            </Card>
          )}
          {renderContent()}
    </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
