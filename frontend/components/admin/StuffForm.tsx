'use client';

import { useState} from 'react';
import Image from 'next/image';
import { Stuff, StuffCreate, StuffUpdate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';

interface StuffFormData {
  kinopoisk_id: string;
  name: string;
  original_name: string;
  career: string;
  ganres: string;
  height: string;
  birthday_day_month: string;
  zodiac: string;
  age: string;
  birthplace: string;
  spouse: string;
  children: string;
  total_films: string;
  career_start_year: string;
  career_end_year: string;
  image: string;
}

interface StuffFormProps {
  stuff?: Stuff | null;
  onSubmit: (data: StuffCreate | StuffUpdate) => void;
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

export default function StuffForm({ stuff, onSubmit, onCancel }: StuffFormProps) {
  const [formData, setFormData] = useState<StuffFormData>({
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
    const submitData: StuffCreate | StuffUpdate = {
      ...(stuff ? {} : { kinopoisk_id: formData.kinopoisk_id }),
      name: formData.name || null,
      original_name: formData.original_name || null,
      age: formData.age ? parseInt(formData.age) : null,
      total_films: formData.total_films ? parseInt(formData.total_films) : null,
      career_start_year: formData.career_start_year ? parseInt(formData.career_start_year) : null,
      career_end_year: formData.career_end_year ? parseInt(formData.career_end_year) : null,
      career: formData.career ? formData.career.split(',').map((s: string) => s.trim()).filter(Boolean) : null,
      ganres: formData.ganres ? formData.ganres.split(',').map((s: string) => s.trim()).filter(Boolean) : null,
      birthplace: formData.birthplace ? formData.birthplace.split(',').map((s: string) => s.trim()).filter(Boolean) : null,
      spouse: formData.spouse ? formData.spouse.split(',').map((s: string) => s.trim()).filter(Boolean) : null,
      children: formData.children ? formData.children.split(',').map((s: string) => s.trim()).filter(Boolean) : null,
      height: formData.height || null,
      birthday_day_month: formData.birthday_day_month || null,
      zodiac: formData.zodiac || null,
      image: formData.image || null,
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="kinopoisk_id">Kinopoisk ID</Label>
          <Input
            id="kinopoisk_id"
            value={formData.kinopoisk_id}
            onChange={(e) => setFormData({ ...formData, kinopoisk_id: e.target.value })}
            required
          />
        </div>
        <div className="space-y-2">
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
        <div className="space-y-2">
          <Label htmlFor="name">Имя</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="original_name">Оригинальное имя</Label>
          <Input
            id="original_name"
            value={formData.original_name}
            onChange={(e) => setFormData({ ...formData, original_name: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="height">Рост</Label>
          <Input
            id="height"
            placeholder="180 см"
            value={formData.height}
            onChange={(e) => setFormData({ ...formData, height: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="zodiac">Знак зодиака</Label>
          <Input
            id="zodiac"
            value={formData.zodiac}
            onChange={(e) => setFormData({ ...formData, zodiac: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="birthday_day_month">День рождения</Label>
          <Input
            id="birthday_day_month"
            placeholder="15 июня"
            value={formData.birthday_day_month}
            onChange={(e) => setFormData({ ...formData, birthday_day_month: e.target.value })}
          />
        </div>
        <div className="space-y-2">
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
        <div className="space-y-2">
          <Label htmlFor="career_start_year">Начало карьеры</Label>
          <Input
            id="career_start_year"
            type="number"
            value={formData.career_start_year}
            onChange={(e) => setFormData({ ...formData, career_start_year: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="career_end_year">Конец карьеры</Label>
          <Input
            id="career_end_year"
            type="number"
            value={formData.career_end_year}
            onChange={(e) => setFormData({ ...formData, career_end_year: e.target.value })}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="career">Карьера (через запятую)</Label>
        <Input
          id="career"
          placeholder="Актер, Режиссер, Продюсер"
          value={formData.career}
          onChange={(e) => setFormData({ ...formData, career: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="ganres">Жанры (через запятую)</Label>
        <Input
          id="ganres"
          placeholder="Драма, Комедия, Боевик"
          value={formData.ganres}
          onChange={(e) => setFormData({ ...formData, ganres: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="birthplace">Место рождения (через запятую)</Label>
        <Input
          id="birthplace"
          placeholder="Москва, Россия"
          value={formData.birthplace}
          onChange={(e) => setFormData({ ...formData, birthplace: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="spouse">Супруг(а) (через запятую)</Label>
        <Input
          id="spouse"
          placeholder="Имя супруги"
          value={formData.spouse}
          onChange={(e) => setFormData({ ...formData, spouse: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="children">Дети (через запятую)</Label>
        <Input
          id="children"
          placeholder="Имена детей"
          value={formData.children}
          onChange={(e) => setFormData({ ...formData, children: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="image">Ссылка на фото</Label>
        <div className="space-y-2">
          <Input
            id="image"
            value={formData.image}
            onChange={(e) => setFormData({ ...formData, image: e.target.value })}
          />
          {formData.image && (
            <div className="relative w-full h-64 rounded-lg overflow-hidden border">
              <Image
                src={normalizeImageUrl(formData.image)}
                alt="Фото участника"
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