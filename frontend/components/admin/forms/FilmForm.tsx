'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { 
  FilmWithDetails, 
  FilmCreate, 
  FilmUpdate,
  SimilarFilmRead,
  SimilarFilmCreate,
  SimilarFilmUpdate,
  FilmStill,
  FilmStillCreate,
  FilmStillUpdate,
  FilmWatchProviderRead,
  FilmWatchProviderCreate,
  FilmWatchProviderUpdate,
  FilmGenreRead,
  FilmGenreCreate,
  FilmCountryRead,
  FilmCountryCreate,
  FilmStuffRead,
  FilmStuffCreate,
  FilmStuffUpdate,
  Genre,
  Country,
  Stuff,
} from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Separator } from '@/components/ui/separator';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { AdminAPI } from '@/lib/api';
import { Plus, Edit, Trash2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

interface FilmFormData {
  kinopoisk_id: string;
  title: string;
  original_title: string;
  description: string;
  full_description: string;
  year: string;
  tagline: string;
  poster: string;
  duration: string;
  rating_kp: string;
  rating_imdb: string;
  budget: string;
  rus_box_office: string;
  usa_box_office: string;
  ru_premiere: string;
  world_premiere: string;
  content_rating: string;
  is_family_friendly: boolean;
  kp_votes_count: string;
  imdb_votes_count: string;
  user_rating: string;
  user_rating_count: string;
}

interface FilmFormProps {
  film?: FilmWithDetails | null;
  onSubmit: (data: FilmCreate | FilmUpdate) => void;
  onCancel: () => void;
}

// Функция для нормализации URL (добавляет протокол, если его нет)
const normalizeImageUrl = (url: string): string => {
  if (!url) return '';
  if (url.startsWith('//')) {
    return `https:${url}`;
  }
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return `https://${url}`;
  }
  return url;
};

export default function FilmForm({ film, onSubmit, onCancel }: FilmFormProps) {
  const [formData, setFormData] = useState<FilmFormData>({
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
    ru_premiere: film?.ru_premiere || '',
    world_premiere: film?.world_premiere || '',
    content_rating: film?.content_rating || '',
    is_family_friendly: film?.is_family_friendly ?? false,
    kp_votes_count: film?.kp_votes_count || '',
    imdb_votes_count: film?.imdb_votes_count || '',
    user_rating: film?.user_rating?.toString() || '',
    user_rating_count: film?.user_rating_count?.toString() || '',
  });

  // Состояния для связанных сущностей
  const [similarFilms, setSimilarFilms] = useState<SimilarFilmRead[]>([]);
  const [filmStills, setFilmStills] = useState<FilmStill[]>([]);
  const [filmWatchProviders, setFilmWatchProviders] = useState<FilmWatchProviderRead[]>([]);
  const [filmGenres, setFilmGenres] = useState<FilmGenreRead[]>([]);
  const [filmCountries, setFilmCountries] = useState<FilmCountryRead[]>([]);
  const [filmStuff, setFilmStuff] = useState<FilmStuffRead[]>([]);
  
  // Справочники
  const [genres, setGenres] = useState<Genre[]>([]);
  const [countries, setCountries] = useState<Country[]>([]);
  const [stuff, setStuff] = useState<Stuff[]>([]);

  // Состояния для редактирования
  const [editingSimilarFilm, setEditingSimilarFilm] = useState<SimilarFilmRead | null>(null);
  const [editingFilmStill, setEditingFilmStill] = useState<FilmStill | null>(null);
  const [editingFilmWatchProvider, setEditingFilmWatchProvider] = useState<FilmWatchProviderRead | null>(null);
  const [editingFilmStuff, setEditingFilmStuff] = useState<FilmStuffRead | null>(null);

  // Формы для создания/редактирования
  const [similarFilmForm, setSimilarFilmForm] = useState<SimilarFilmCreate>({
    film_id: film?.id || 0,
    similar_film_id: '',
    similar_film_title: '',
    similar_film_year: null,
    similar_film_genres: null,
    similar_film_poster: null,
    similar_film_rating: null,
  });

  const [filmStillForm, setFilmStillForm] = useState<FilmStillCreate>({
    film_id: film?.id || 0,
    picture_id: '',
    original_url: '',
    source: 'stills',
  });

  const [filmWatchProviderForm, setFilmWatchProviderForm] = useState<FilmWatchProviderCreate>({
    film_id: film?.id || 0,
    name: '',
    url: '',
    logo: null,
  });

  const [filmGenreForm, setFilmGenreForm] = useState<FilmGenreCreate>({
    film_id: film?.id || 0,
    genre_id: 0,
  });

  const [filmCountryForm, setFilmCountryForm] = useState<FilmCountryCreate>({
    film_id: film?.id || 0,
    country_id: 0,
  });

  const [filmStuffForm, setFilmStuffForm] = useState<FilmStuffCreate>({
    film_id: film?.id || 0,
    stuff_id: 0,
    role: null,
  });

  useEffect(() => {
    if (film?.id) {
      loadRelatedData();
      loadReferenceData();
    }
  }, [film?.id]);

  const loadRelatedData = async () => {
    if (!film?.id) return;
    
    try {
      const [similar, stills, providers, genres, countries, stuff] = await Promise.all([
        AdminAPI.getAllSimilarFilms(1, 100).then(data => data.filter(item => item.film_id === film.id)),
        AdminAPI.getAllFilmStills(1, 100).then(data => data.filter(item => item.film_id === film.id)),
        AdminAPI.getAllFilmWatchProviders(1, 100).then(data => data.filter(item => item.film_id === film.id)),
        AdminAPI.getAllFilmGenres(1, 100).then(data => data.filter(item => item.film_id === film.id)),
        AdminAPI.getAllFilmCountries(1, 100).then(data => data.filter(item => item.film_id === film.id)),
        AdminAPI.getAllFilmStuff(1, 100).then(data => data.filter(item => item.film_id === film.id)),
      ]);
      
      setSimilarFilms(similar);
      setFilmStills(stills);
      setFilmWatchProviders(providers);
      setFilmGenres(genres);
      setFilmCountries(countries);
      setFilmStuff(stuff);
    } catch (error) {
      console.error('Error loading related data:', error);
    }
  };

  const loadReferenceData = async () => {
    try {
      const [genresData, countriesData, stuffData] = await Promise.all([
        AdminAPI.getAllGenres(),
        AdminAPI.getAllCountries(),
        AdminAPI.getAllStuffAll(),
      ]);
      
      setGenres(genresData);
      setCountries(countriesData);
      setStuff(Array.isArray(stuffData) ? stuffData : []);
    } catch (error) {
      console.error('Error loading reference data:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const submitData: FilmCreate | FilmUpdate = {
      ...(film ? {} : { kinopoisk_id: formData.kinopoisk_id }),
      title: formData.title || null,
      original_title: formData.original_title || null,
      description: formData.description || null,
      full_description: formData.full_description || null,
      year: formData.year ? parseInt(formData.year) : null,
      tagline: formData.tagline || null,
      poster: formData.poster || null,
      duration: formData.duration || null,
      rating_kp: formData.rating_kp ? parseFloat(formData.rating_kp) : null,
      rating_imdb: formData.rating_imdb ? parseFloat(formData.rating_imdb) : null,
      budget: formData.budget || null,
      rus_box_office: formData.rus_box_office || null,
      usa_box_office: formData.usa_box_office || null,
      ru_premiere: formData.ru_premiere || null,
      world_premiere: formData.world_premiere || null,
      content_rating: formData.content_rating || null,
      is_family_friendly: formData.is_family_friendly,
      kp_votes_count: formData.kp_votes_count || null,
      imdb_votes_count: formData.imdb_votes_count || null,
      user_rating: formData.user_rating ? parseFloat(formData.user_rating) : null,
      user_rating_count: formData.user_rating_count ? parseInt(formData.user_rating_count) : null,
    };
    onSubmit(submitData);
  };

  // Обработчики для похожих фильмов
  const handleSimilarFilmSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!film?.id) return;
    
    try {
      if (editingSimilarFilm) {
        await AdminAPI.updateSimilarFilm(editingSimilarFilm.id, similarFilmForm);
      } else {
        await AdminAPI.createSimilarFilm({ ...similarFilmForm, film_id: film.id });
      }
      setEditingSimilarFilm(null);
      setSimilarFilmForm({
        film_id: film.id,
        similar_film_id: '',
        similar_film_title: '',
        similar_film_year: null,
        similar_film_genres: null,
        similar_film_poster: null,
        similar_film_rating: null,
      });
      loadRelatedData();
    } catch (error) {
      console.error('Error saving similar film:', error);
    }
  };

  const handleDeleteSimilarFilm = async (id: number) => {
    if (!confirm('Удалить похожий фильм?')) return;
    try {
      await AdminAPI.deleteSimilarFilm(id);
      loadRelatedData();
    } catch (error) {
      console.error('Error deleting similar film:', error);
    }
  };

  // Обработчики для кадров
  const handleFilmStillSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!film?.id) return;
    
    try {
      if (editingFilmStill) {
        await AdminAPI.updateFilmStill(editingFilmStill.id, filmStillForm);
      } else {
        await AdminAPI.createFilmStill({ ...filmStillForm, film_id: film.id });
      }
      setEditingFilmStill(null);
      setFilmStillForm({
        film_id: film.id,
        picture_id: '',
        original_url: '',
        source: 'stills',
      });
      loadRelatedData();
    } catch (error) {
      console.error('Error saving film still:', error);
    }
  };

  const handleDeleteFilmStill = async (id: number) => {
    if (!confirm('Удалить кадр?')) return;
    try {
      await AdminAPI.deleteFilmStill(id);
      loadRelatedData();
    } catch (error) {
      console.error('Error deleting film still:', error);
    }
  };

  // Обработчики для провайдеров
  const handleFilmWatchProviderSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!film?.id) return;
    
    try {
      if (editingFilmWatchProvider) {
        await AdminAPI.updateFilmWatchProvider(editingFilmWatchProvider.id, filmWatchProviderForm);
      } else {
        await AdminAPI.createFilmWatchProvider({ ...filmWatchProviderForm, film_id: film.id });
      }
      setEditingFilmWatchProvider(null);
      setFilmWatchProviderForm({
        film_id: film.id,
        name: '',
        url: '',
        logo: null,
      });
      loadRelatedData();
    } catch (error) {
      console.error('Error saving film watch provider:', error);
    }
  };

  const handleDeleteFilmWatchProvider = async (id: number) => {
    if (!confirm('Удалить провайдера?')) return;
    try {
      await AdminAPI.deleteFilmWatchProvider(id);
      loadRelatedData();
    } catch (error) {
      console.error('Error deleting film watch provider:', error);
    }
  };

  // Обработчики для жанров
  const handleFilmGenreSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!film?.id || !filmGenreForm.genre_id) return;
    
    try {
      await AdminAPI.createFilmGenre({ ...filmGenreForm, film_id: film.id });
      setFilmGenreForm({ film_id: film.id, genre_id: 0 });
      loadRelatedData();
    } catch (error) {
      console.error('Error saving film genre:', error);
    }
  };

  const handleDeleteFilmGenre = async (id: number) => {
    if (!confirm('Удалить жанр?')) return;
    try {
      await AdminAPI.deleteFilmGenre(id);
      loadRelatedData();
    } catch (error) {
      console.error('Error deleting film genre:', error);
    }
  };

  // Обработчики для стран
  const handleFilmCountrySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!film?.id || !filmCountryForm.country_id) return;
    
    try {
      await AdminAPI.createFilmCountry({ ...filmCountryForm, film_id: film.id });
      setFilmCountryForm({ film_id: film.id, country_id: 0 });
      loadRelatedData();
    } catch (error) {
      console.error('Error saving film country:', error);
    }
  };

  const handleDeleteFilmCountry = async (id: number) => {
    if (!confirm('Удалить страну?')) return;
    try {
      await AdminAPI.deleteFilmCountry(id);
      loadRelatedData();
    } catch (error) {
      console.error('Error deleting film country:', error);
    }
  };

  // Обработчики для участников
  const handleFilmStuffSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!film?.id || !filmStuffForm.stuff_id) return;
    
    try {
      if (editingFilmStuff) {
        await AdminAPI.updateFilmStuff(editingFilmStuff.id, { role: filmStuffForm.role });
      } else {
        await AdminAPI.createFilmStuff({ ...filmStuffForm, film_id: film.id });
      }
      setEditingFilmStuff(null);
      setFilmStuffForm({
        film_id: film.id,
        stuff_id: 0,
        role: null,
      });
      loadRelatedData();
    } catch (error) {
      console.error('Error saving film stuff:', error);
    }
  };

  const handleDeleteFilmStuff = async (id: number) => {
    if (!confirm('Удалить участника?')) return;
    try {
      await AdminAPI.deleteFilmStuff(id);
      loadRelatedData();
    } catch (error) {
      console.error('Error deleting film stuff:', error);
    }
  };

  // Рендер основной формы
  const renderMainForm = () => (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="kinopoisk_id">Kinopoisk ID</Label>
          <Input
            id="kinopoisk_id"
            value={formData.kinopoisk_id}
            onChange={(e) => setFormData({ ...formData, kinopoisk_id: e.target.value })}
            required={!film}
            disabled={!!film}
          />
        </div>
        <div className="space-y-2">
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
        <div className="space-y-2">
          <Label htmlFor="title">Название</Label>
          <Input
            id="title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="original_title">Оригинальное название</Label>
          <Input
            id="original_title"
            value={formData.original_title}
            onChange={(e) => setFormData({ ...formData, original_title: e.target.value })}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="tagline">Слоган</Label>
        <Input
          id="tagline"
          value={formData.tagline}
          onChange={(e) => setFormData({ ...formData, tagline: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Краткое описание</Label>
        <Textarea
          id="description"
          rows={3}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="full_description">Полное описание</Label>
        <Textarea
          id="full_description"
          rows={5}
          value={formData.full_description}
          onChange={(e) => setFormData({ ...formData, full_description: e.target.value })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="duration">Длительность</Label>
          <Input
            id="duration"
            placeholder="120 мин"
            value={formData.duration}
            onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="content_rating">Возрастной рейтинг</Label>
          <Input
            id="content_rating"
            placeholder="16+"
            value={formData.content_rating}
            onChange={(e) => setFormData({ ...formData, content_rating: e.target.value })}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="poster">Ссылка на постер</Label>
        <div className="space-y-2">
          <Input
            id="poster"
            value={formData.poster}
            onChange={(e) => setFormData({ ...formData, poster: e.target.value })}
          />
          {formData.poster && (
            <div className="relative w-full h-64 rounded-lg overflow-hidden border">
              <Image
                src={normalizeImageUrl(formData.poster)}
                alt="Постер фильма"
                fill
                className="object-contain"
                unoptimized={false}
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }}
              />
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="ru_premiere">Премьера в России</Label>
          <Input
            id="ru_premiere"
            placeholder="2024-01-01"
            value={formData.ru_premiere}
            onChange={(e) => setFormData({ ...formData, ru_premiere: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="world_premiere">Мировая премьера</Label>
          <Input
            id="world_premiere"
            placeholder="2024-01-01"
            value={formData.world_premiere}
            onChange={(e) => setFormData({ ...formData, world_premiere: e.target.value })}
          />
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <Checkbox
          id="is_family_friendly"
          checked={formData.is_family_friendly}
          onCheckedChange={(checked) => 
            setFormData({ ...formData, is_family_friendly: checked as boolean })
          }
        />
        <Label htmlFor="is_family_friendly" className="cursor-pointer">
          Семейный фильм
        </Label>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
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
        <div className="space-y-2">
          <Label htmlFor="kp_votes_count">Количество голосов КП</Label>
          <Input
            id="kp_votes_count"
            value={formData.kp_votes_count}
            onChange={(e) => setFormData({ ...formData, kp_votes_count: e.target.value })}
            placeholder="100000"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
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
        <div className="space-y-2">
          <Label htmlFor="imdb_votes_count">Количество голосов IMDb</Label>
          <Input
            id="imdb_votes_count"
            value={formData.imdb_votes_count}
            onChange={(e) => setFormData({ ...formData, imdb_votes_count: e.target.value })}
            placeholder="50000"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="user_rating">Пользовательский рейтинг</Label>
          <Input
            id="user_rating"
            type="number"
            step="0.1"
            min="0"
            max="10"
            value={formData.user_rating}
            onChange={(e) => setFormData({ ...formData, user_rating: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="user_rating_count">Количество пользовательских оценок</Label>
          <Input
            id="user_rating_count"
            type="number"
            value={formData.user_rating_count}
            onChange={(e) => setFormData({ ...formData, user_rating_count: e.target.value })}
            placeholder="1000"
          />
        </div>
      </div>

      <div className="space-y-4">
        <Label>Кассовые сборы</Label>
        <div className="grid grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label htmlFor="budget">Бюджет</Label>
            <Input
              id="budget"
              placeholder="$50,000,000"
              value={formData.budget}
              onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="usa_box_office">Сборы в США</Label>
            <Input
              id="usa_box_office"
              placeholder="$100,000,000"
              value={formData.usa_box_office}
              onChange={(e) => setFormData({ ...formData, usa_box_office: e.target.value })}
            />
          </div>
          <div className="space-y-2">
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

  if (!film?.id) {
    // Если фильм еще не создан, показываем только основную форму
    return renderMainForm();
  }

  return (
    <Tabs defaultValue="main" className="w-full">
      <TabsList className="grid w-full grid-cols-7">
        <TabsTrigger value="main">Основное</TabsTrigger>
        <TabsTrigger value="similar">Похожие</TabsTrigger>
        <TabsTrigger value="stills">Кадры</TabsTrigger>
        <TabsTrigger value="providers">Провайдеры</TabsTrigger>
        <TabsTrigger value="genres">Жанры</TabsTrigger>
        <TabsTrigger value="countries">Страны</TabsTrigger>
        <TabsTrigger value="stuff">Участники</TabsTrigger>
      </TabsList>

      <TabsContent value="main" className="space-y-6">
        {renderMainForm()}
      </TabsContent>

      <TabsContent value="similar" className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Похожие фильмы</h3>
            <Button
              onClick={() => {
                setEditingSimilarFilm(null);
                setSimilarFilmForm({
                  film_id: film.id,
                  similar_film_id: '',
                  similar_film_title: '',
                  similar_film_year: null,
                  similar_film_genres: null,
                  similar_film_poster: null,
                  similar_film_rating: null,
                });
              }}
            >
              <Plus className="h-4 w-4 mr-2" />
              Добавить
            </Button>
          </div>

          {(editingSimilarFilm !== null || (!editingSimilarFilm && similarFilmForm.similar_film_id === '')) && (
            <form onSubmit={handleSimilarFilmSubmit} className="space-y-4 p-4 border rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Kinopoisk ID похожего фильма</Label>
                  <Input
                    value={similarFilmForm.similar_film_id}
                    onChange={(e) => setSimilarFilmForm({ ...similarFilmForm, similar_film_id: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label>Название</Label>
                  <Input
                    value={similarFilmForm.similar_film_title}
                    onChange={(e) => setSimilarFilmForm({ ...similarFilmForm, similar_film_title: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Год</Label>
                  <Input
                    value={similarFilmForm.similar_film_year || ''}
                    onChange={(e) => setSimilarFilmForm({ ...similarFilmForm, similar_film_year: e.target.value || null })}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Рейтинг</Label>
                  <Input
                    value={similarFilmForm.similar_film_rating || ''}
                    onChange={(e) => setSimilarFilmForm({ ...similarFilmForm, similar_film_rating: e.target.value || null })}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Жанры (через запятую)</Label>
                <Input
                  value={similarFilmForm.similar_film_genres?.join(', ') || ''}
                  onChange={(e) => setSimilarFilmForm({ 
                    ...similarFilmForm, 
                    similar_film_genres: e.target.value ? e.target.value.split(',').map(s => s.trim()) : null 
                  })}
                />
              </div>
              <div className="space-y-2">
                <Label>URL постера</Label>
                <Input
                  value={similarFilmForm.similar_film_poster || ''}
                  onChange={(e) => setSimilarFilmForm({ ...similarFilmForm, similar_film_poster: e.target.value || null })}
                />
              </div>
              <div className="flex space-x-2">
                <Button type="submit">Сохранить</Button>
                <Button type="button" variant="outline" onClick={() => setEditingSimilarFilm(null)}>
                  Отмена
                </Button>
              </div>
            </form>
          )}

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Kinopoisk ID</TableHead>
                <TableHead>Название</TableHead>
                <TableHead>Год</TableHead>
                <TableHead>Рейтинг</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {similarFilms.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.id}</TableCell>
                  <TableCell>{item.similar_film_id}</TableCell>
                  <TableCell>{item.similar_film_title}</TableCell>
                  <TableCell>{item.similar_film_year || '-'}</TableCell>
                  <TableCell>{item.similar_film_rating || '-'}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setEditingSimilarFilm(item);
                          setSimilarFilmForm({
                            film_id: film.id,
                            similar_film_id: item.similar_film_id,
                            similar_film_title: item.similar_film_title,
                            similar_film_year: item.similar_film_year,
                            similar_film_genres: item.similar_film_genres,
                            similar_film_poster: item.similar_film_poster,
                            similar_film_rating: item.similar_film_rating,
                          });
                        }}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteSimilarFilm(item.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </TabsContent>

      <TabsContent value="stills" className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Кадры из фильма</h3>
            <Button
              onClick={() => {
                setEditingFilmStill(null);
                setFilmStillForm({
                  film_id: film.id,
                  picture_id: '',
                  original_url: '',
                  source: 'stills',
                });
              }}
            >
              <Plus className="h-4 w-4 mr-2" />
              Добавить
            </Button>
          </div>

          {(editingFilmStill !== null || (!editingFilmStill && filmStillForm.picture_id === '')) && (
            <form onSubmit={handleFilmStillSubmit} className="space-y-4 p-4 border rounded-lg">
              <div className="space-y-2">
                <Label>ID изображения</Label>
                <Input
                  value={filmStillForm.picture_id}
                  onChange={(e) => setFilmStillForm({ ...filmStillForm, picture_id: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>URL изображения</Label>
                <Input
                  value={filmStillForm.original_url}
                  onChange={(e) => setFilmStillForm({ ...filmStillForm, original_url: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Источник</Label>
                <Select
                  value={filmStillForm.source}
                  onValueChange={(value) => setFilmStillForm({ ...filmStillForm, source: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="stills">Кадры</SelectItem>
                    <SelectItem value="wall">Обои</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex space-x-2">
                <Button type="submit">Сохранить</Button>
                <Button type="button" variant="outline" onClick={() => setEditingFilmStill(null)}>
                  Отмена
                </Button>
              </div>
            </form>
          )}

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>ID изображения</TableHead>
                <TableHead>Источник</TableHead>
                <TableHead>URL</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filmStills.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.id}</TableCell>
                  <TableCell>{item.picture_id}</TableCell>
                  <TableCell>
                    <Badge>{item.source}</Badge>
                  </TableCell>
                  <TableCell className="max-w-[200px] truncate">{item.original_url}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setEditingFilmStill(item);
                          setFilmStillForm({
                            film_id: film.id,
                            picture_id: item.picture_id,
                            original_url: item.original_url,
                            source: item.source,
                          });
                        }}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteFilmStill(item.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </TabsContent>

      <TabsContent value="providers" className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Провайдеры просмотра</h3>
            <Button
              onClick={() => {
                setEditingFilmWatchProvider(null);
                setFilmWatchProviderForm({
                  film_id: film.id,
                  name: '',
                  url: '',
                  logo: null,
                });
              }}
            >
              <Plus className="h-4 w-4 mr-2" />
              Добавить
            </Button>
          </div>

          {(editingFilmWatchProvider !== null || (!editingFilmWatchProvider && filmWatchProviderForm.name === '')) && (
            <form onSubmit={handleFilmWatchProviderSubmit} className="space-y-4 p-4 border rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Название провайдера</Label>
                  <Input
                    value={filmWatchProviderForm.name}
                    onChange={(e) => setFilmWatchProviderForm({ ...filmWatchProviderForm, name: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label>URL</Label>
                  <Input
                    value={filmWatchProviderForm.url}
                    onChange={(e) => setFilmWatchProviderForm({ ...filmWatchProviderForm, url: e.target.value })}
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>URL логотипа</Label>
                <Input
                  value={filmWatchProviderForm.logo || ''}
                  onChange={(e) => setFilmWatchProviderForm({ ...filmWatchProviderForm, logo: e.target.value || null })}
                />
              </div>
              <div className="flex space-x-2">
                <Button type="submit">Сохранить</Button>
                <Button type="button" variant="outline" onClick={() => setEditingFilmWatchProvider(null)}>
                  Отмена
                </Button>
              </div>
            </form>
          )}

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Название</TableHead>
                <TableHead>URL</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filmWatchProviders.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.id}</TableCell>
                  <TableCell>{item.name}</TableCell>
                  <TableCell className="max-w-[200px] truncate">{item.url}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setEditingFilmWatchProvider(item);
                          setFilmWatchProviderForm({
                            film_id: film.id,
                            name: item.name,
                            url: item.url,
                            logo: item.logo,
                          });
                        }}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteFilmWatchProvider(item.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </TabsContent>

      <TabsContent value="genres" className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Жанры фильма</h3>
          </div>

          <form onSubmit={handleFilmGenreSubmit} className="space-y-4 p-4 border rounded-lg">
            <div className="space-y-2">
              <Label>Жанр</Label>
              <Select
                value={filmGenreForm.genre_id.toString()}
                onValueChange={(value) => setFilmGenreForm({ ...filmGenreForm, genre_id: parseInt(value) })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите жанр" />
                </SelectTrigger>
                <SelectContent>
                  {genres.map((genre) => (
                    <SelectItem key={genre.id} value={genre.id.toString()}>
                      {genre.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" disabled={!filmGenreForm.genre_id}>
              <Plus className="h-4 w-4 mr-2" />
              Добавить жанр
            </Button>
          </form>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Жанр</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filmGenres.map((item) => {
                const genre = genres.find(g => g.id === item.genre_id);
                return (
                  <TableRow key={item.id}>
                    <TableCell>{item.id}</TableCell>
                    <TableCell>{genre?.name || `ID: ${item.genre_id}`}</TableCell>
                    <TableCell>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteFilmGenre(item.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </TabsContent>

      <TabsContent value="countries" className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Страны фильма</h3>
          </div>

          <form onSubmit={handleFilmCountrySubmit} className="space-y-4 p-4 border rounded-lg">
            <div className="space-y-2">
              <Label>Страна</Label>
              <Select
                value={filmCountryForm.country_id.toString()}
                onValueChange={(value) => setFilmCountryForm({ ...filmCountryForm, country_id: parseInt(value) })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите страну" />
                </SelectTrigger>
                <SelectContent>
                  {countries.map((country) => (
                    <SelectItem key={country.id} value={country.id.toString()}>
                      {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" disabled={!filmCountryForm.country_id}>
              <Plus className="h-4 w-4 mr-2" />
              Добавить страну
            </Button>
          </form>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Страна</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filmCountries.map((item) => {
                const country = countries.find(c => c.id === item.country_id);
                return (
                  <TableRow key={item.id}>
                    <TableCell>{item.id}</TableCell>
                    <TableCell>{country?.name || `ID: ${item.country_id}`}</TableCell>
                    <TableCell>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteFilmCountry(item.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </TabsContent>

      <TabsContent value="stuff" className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Участники фильма</h3>
            <Button
              onClick={() => {
                setEditingFilmStuff(null);
                setFilmStuffForm({
                  film_id: film.id,
                  stuff_id: 0,
                  role: null,
                });
              }}
            >
              <Plus className="h-4 w-4 mr-2" />
              Добавить
            </Button>
          </div>

          {(editingFilmStuff !== null || (!editingFilmStuff && filmStuffForm.stuff_id === 0)) && (
            <form onSubmit={handleFilmStuffSubmit} className="space-y-4 p-4 border rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Участник</Label>
                  <Select
                    value={filmStuffForm.stuff_id.toString()}
                    onValueChange={(value) => setFilmStuffForm({ ...filmStuffForm, stuff_id: parseInt(value) })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Выберите участника" />
                    </SelectTrigger>
                    <SelectContent>
                      {stuff.map((s) => (
                        <SelectItem key={s.id} value={s.id.toString()}>
                          {s.name || s.original_name || `ID: ${s.id}`}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Роль</Label>
                  <Input
                    value={filmStuffForm.role || ''}
                    onChange={(e) => setFilmStuffForm({ ...filmStuffForm, role: e.target.value || null })}
                    placeholder="actor, director, writer..."
                  />
                </div>
              </div>
              <div className="flex space-x-2">
                <Button type="submit" disabled={!filmStuffForm.stuff_id}>
                  Сохранить
                </Button>
                <Button type="button" variant="outline" onClick={() => setEditingFilmStuff(null)}>
                  Отмена
                </Button>
              </div>
            </form>
          )}

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Участник</TableHead>
                <TableHead>Роль</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filmStuff.map((item) => {
                const person = stuff.find(s => s.id === item.stuff_id);
                return (
                  <TableRow key={item.id}>
                    <TableCell>{item.id}</TableCell>
                    <TableCell>{person?.name || person?.original_name || `ID: ${item.stuff_id}`}</TableCell>
                    <TableCell>{item.role || '-'}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setEditingFilmStuff(item);
                            setFilmStuffForm({
                              film_id: film.id,
                              stuff_id: item.stuff_id,
                              role: item.role,
                            });
                          }}
                        >
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteFilmStuff(item.id)}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </TabsContent>
    </Tabs>
  );
}
