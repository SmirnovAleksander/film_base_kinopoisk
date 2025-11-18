'use client';

import { useState } from 'react';
import { Country, CountryCreate, CountryUpdate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';

interface CountryFormData {
  name: string;
}

interface CountryFormProps {
  country?: Country | null;
  onSubmit: (data: CountryCreate | CountryUpdate) => void;
  onCancel: () => void;
}

export default function CountryForm({ country, onSubmit, onCancel }: CountryFormProps) {
  const [formData, setFormData] = useState<CountryFormData>({
    name: country?.name || '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const submitData: CountryCreate | CountryUpdate = {
      name: formData.name.trim(),
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="name">Название страны</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="Россия"
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

