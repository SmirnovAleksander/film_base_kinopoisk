'use client';

import { useState } from 'react';
import { Genre, GenreCreate, GenreUpdate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';

interface GenreFormData {
  name: string;
}

interface GenreFormProps {
  genre?: Genre | null;
  onSubmit: (data: GenreCreate | GenreUpdate) => void;
  onCancel: () => void;
}

export default function GenreForm({ genre, onSubmit, onCancel }: GenreFormProps) {
  const [formData, setFormData] = useState<GenreFormData>({
    name: genre?.name || '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const submitData: GenreCreate | GenreUpdate = {
      name: formData.name.trim(),
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="name">Название жанра</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="Драма"
          required
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

