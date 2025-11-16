'use client';

import { useState } from 'react';
import { FilmWithDetails, Stuff } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Separator } from '@/components/ui/separator';

export default function FilmForm({ film, onSubmit, onCancel }: any) {
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
