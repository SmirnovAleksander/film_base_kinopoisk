'use client';

import { useState, useEffect } from 'react';
import { AdminAPI } from '@/lib/api';
import { FilmWithDetails, Stuff, Genre, Country, Media, User } from '@/lib/types';
import { Card, CardContent } from '@/components/ui/card';
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar';
import FilmsSection from '@/components/admin/sections/FilmsSection';
import StuffSection from '@/components/admin/sections/StuffSection';
import GenresSection from '@/components/admin/sections/GenresSection';
import CountriesSection from '@/components/admin/sections/CountriesSection';
import MediaSection from '@/components/admin/sections/MediaSection';
import UsersSection from '@/components/admin/sections/UsersSection';
import { AdminSidebar } from '@/components/admin/AdminSidebar';

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
  const [editingFilm, setEditingFilm] = useState<FilmWithDetails | null | undefined>(undefined);
  const [editingStuff, setEditingStuff] = useState<Stuff | null | undefined>(undefined);
  const [editingGenre, setEditingGenre] = useState<Genre | null | undefined>(undefined);
  const [editingCountry, setEditingCountry] = useState<Country | null | undefined>(undefined);
  const [editingMedia, setEditingMedia] = useState<Media | null | undefined>(undefined);
  const [editingUser, setEditingUser] = useState<User | null | undefined>(undefined);
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
      setEditingFilm(undefined);
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
      setEditingStuff(undefined);
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
      setEditingGenre(undefined);
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
      setEditingCountry(undefined);
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
      setEditingMedia(undefined);
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
      setEditingUser(undefined);
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

  const renderContent = () => {
    switch (activeTab) {
      case '#films':
        return (
          <FilmsSection
            films={films}
            editingFilm={editingFilm}
            setEditingFilm={setEditingFilm}
            onSubmit={handleFilmSubmit}
            onDelete={handleDeleteFilm}
          />
        );
      case '#stuff':
        return (
          <StuffSection
            stuff={stuff}
            editingStuff={editingStuff}
            setEditingStuff={setEditingStuff}
            onSubmit={handleStuffSubmit}
            onDelete={handleDeleteStuff}
          />
        );
      case '#genres':
        return (
          <GenresSection
            genres={genres}
            editingGenre={editingGenre}
            setEditingGenre={setEditingGenre}
            onSubmit={handleGenreSubmit}
            onDelete={handleDeleteGenre}
          />
        );
      case '#countries':
        return (
          <CountriesSection
            countries={countries}
            editingCountry={editingCountry}
            setEditingCountry={setEditingCountry}
            onSubmit={handleCountrySubmit}
            onDelete={handleDeleteCountry}
          />
        );
      case '#media':
        return (
          <MediaSection
            media={media}
            editingMedia={editingMedia}
            setEditingMedia={setEditingMedia}
            onSubmit={handleMediaSubmit}
            onDelete={handleDeleteMedia}
          />
        );
      case '#users':
        return (
          <UsersSection
            users={users}
            editingUser={editingUser}
            setEditingUser={setEditingUser}
            onSubmit={handleUserSubmit}
            onDelete={handleDeleteUser}
          />
        );
      default:
        return (
          <FilmsSection
            films={films}
            editingFilm={editingFilm}
            setEditingFilm={setEditingFilm}
            onSubmit={handleFilmSubmit}
            onDelete={handleDeleteFilm}
          />
        );
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
