'use client';

import { useState } from 'react';
import Image from 'next/image';
import { FilmWithDetails, FilmCreate, FilmUpdate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Separator } from '@/components/ui/separator';
import { Checkbox } from '@/components/ui/checkbox';

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
          <Label htmlFor="content_rating">Возрастной рейтинг</Label>
          <Input
            id="content_rating"
            placeholder="16+"
            value={formData.content_rating}
            onChange={(e) => setFormData({ ...formData, content_rating: e.target.value })}
          />
        </div>
      </div>

      <div>
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
        <div>
          <Label htmlFor="ru_premiere">Премьера в России</Label>
          <Input
            id="ru_premiere"
            placeholder="2024-01-01"
            value={formData.ru_premiere}
            onChange={(e) => setFormData({ ...formData, ru_premiere: e.target.value })}
          />
        </div>
        <div>
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
        <div>
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
        <div>
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
        <div>
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
