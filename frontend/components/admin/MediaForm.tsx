'use client';

import { useState } from 'react';
import Image from 'next/image';
import { Media, MediaCreate, MediaUpdate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface MediaFormData {
  url: string;
  title: string;
  image: string;
  category: string;
  date: string;
  card_type: string;
  type: string;
}

interface MediaFormProps {
  media?: Media | null;
  onSubmit: (data: MediaCreate | MediaUpdate) => void;
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

export default function MediaForm({ media, onSubmit, onCancel }: MediaFormProps) {
  const [formData, setFormData] = useState<MediaFormData>({
    url: media?.url || '',
    title: media?.title || '',
    image: media?.image || '',
    category: media?.category || '',
    date: media?.date || '',
    card_type: media?.card_type || '',
    type: media?.type || 'news',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const submitData: MediaCreate | MediaUpdate = {
      url: formData.url || null,
      title: formData.title || null,
      image: formData.image || null,
      category: formData.category || null,
      date: formData.date || null,
      card_type: formData.card_type || null,
      type: formData.type || null,
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="type">Тип контента</Label>
        <Select
          value={formData.type}
          onValueChange={(value) => setFormData({ ...formData, type: value })}
        >
          <SelectTrigger id="type">
            <SelectValue placeholder="Выберите тип" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="news">Новости</SelectItem>
            <SelectItem value="video">Видео</SelectItem>
            <SelectItem value="game">Игры</SelectItem>
            <SelectItem value="podcast">Подкасты</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="url">URL</Label>
        <Input
          id="url"
          value={formData.url}
          onChange={(e) => setFormData({ ...formData, url: e.target.value })}
          placeholder="https://example.com/article"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="title">Заголовок</Label>
        <Input
          id="title"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          placeholder="Заголовок статьи"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="image">Ссылка на изображение</Label>
        <div className="space-y-2">
          <Input
            id="image"
            value={formData.image}
            onChange={(e) => setFormData({ ...formData, image: e.target.value })}
            placeholder="https://example.com/image.jpg"
          />
          {formData.image && (
            <div className="relative w-full h-64 rounded-lg overflow-hidden border">
              <Image
                src={normalizeImageUrl(formData.image)}
                alt="Изображение медиа"
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
          <Label htmlFor="category">Категория</Label>
          <Input
            id="category"
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            placeholder="Категория"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="card_type">Тип карточки</Label>
          <Input
            id="card_type"
            value={formData.card_type}
            onChange={(e) => setFormData({ ...formData, card_type: e.target.value })}
            placeholder="Тип карточки"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="date">Дата публикации</Label>
        <Input
          id="date"
          value={formData.date}
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          placeholder="2024-01-01"
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

