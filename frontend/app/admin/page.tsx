'use client';

import { useState, useEffect } from 'react';
import { AdminAPI } from '@/lib/api';
import { Film, Stuff } from '@/lib/types/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function AdminPage() {
  const [films, setFilms] = useState<Film[]>([]);
  const [stuff, setStuff] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [editingFilm, setEditingFilm] = useState<Film | null>(null);
  const [editingStuff, setEditingStuff] = useState<any>(null);
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
        AdminAPI.getAllFilms(1, 50),
        AdminAPI.getAllStuff(1, 50)
      ]);
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

  if (isLoading) {
    return <div className="container mx-auto p-6">Загрузка...</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Админ панель</h1>
      
      {message && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {message}
        </div>
      )}
      
      <Tabs defaultValue="films">
        <TabsList>
          <TabsTrigger value="films">Фильмы</TabsTrigger>
          <TabsTrigger value="stuff">Участники</TabsTrigger>
        </TabsList>
        
        <TabsContent value="films">
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold">Управление фильмами</h2>
              <Dialog open={showFilmDialog} onOpenChange={setShowFilmDialog}>
                <DialogTrigger asChild>
                  <Button onClick={() => setEditingFilm(null)}>Добавить фильм</Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>
                      {editingFilm ? 'Редактировать фильм' : 'Добавить фильм'}
                    </DialogTitle>
                  </DialogHeader>
                  <FilmForm
                    film={editingFilm}
                    onSubmit={handleFilmSubmit}
                    onCancel={() => setShowFilmDialog(false)}
                  />
                </DialogContent>
              </Dialog>
            </div>
            
            <div className="grid gap-4">
              {films.map((film) => (
                <Card key={film.id}>
                  <CardHeader>
                    <CardTitle className="flex justify-between items-center">
                      <span>{film.title || film.original_title}</span>
                      <div className="space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setEditingFilm(film);
                            setShowFilmDialog(true);
                          }}
                        >
                          Редактировать
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteFilm(film.id)}
                        >
                          Удалить
                        </Button>
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">{film.description}</p>
                    {film.year && <p className="text-sm mt-2">Год: {film.year}</p>}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="stuff">
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold">Управление участниками</h2>
              <Dialog open={showStuffDialog} onOpenChange={setShowStuffDialog}>
                <DialogTrigger asChild>
                  <Button onClick={() => setEditingStuff(null)}>Добавить участника</Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>
                      {editingStuff ? 'Редактировать участника' : 'Добавить участника'}
                    </DialogTitle>
                  </DialogHeader>
                  <StuffForm
                    stuff={editingStuff}
                    onSubmit={handleStuffSubmit}
                    onCancel={() => setShowStuffDialog(false)}
                  />
                </DialogContent>
              </Dialog>
            </div>
            
            <div className="grid gap-4">
              {stuff?.items?.map((person: any) => (
                <Card key={person.id}>
                  <CardHeader>
                    <CardTitle className="flex justify-between items-center">
                      <span>{person.name || person.original_name}</span>
                      <div className="space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setEditingStuff(person);
                            setShowStuffDialog(true);
                          }}
                        >
                          Редактировать
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteStuff(person.id)}
                        >
                          Удалить
                        </Button>
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">{person.career?.join(', ')}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
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
    year: film?.year || '',
    tagline: film?.tagline || '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
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
      <div>
        <Label htmlFor="description">Описание</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
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
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      career: formData.career.split(',').map((s: string) => s.trim()).filter(Boolean),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
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
      <div>
        <Label htmlFor="career">Карьера (через запятую)</Label>
        <Input
          id="career"
          value={formData.career}
          onChange={(e) => setFormData({ ...formData, career: e.target.value })}
        />
      </div>
      <div className="flex space-x-2">
        <Button type="submit">Сохранить</Button>
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
      </div>
    </form>
  );
}