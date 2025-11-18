'use client';

import { useState } from 'react';
import { User, UserCreate, UserUpdate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Checkbox } from '@/components/ui/checkbox';

interface UserFormData {
  email: string;
  password: string;
  username: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

interface UserFormProps {
  user?: User | null;
  onSubmit: (data: UserCreate | UserUpdate) => void;
  onCancel: () => void;
}

export default function UserForm({ user, onSubmit, onCancel }: UserFormProps) {
  const [formData, setFormData] = useState<UserFormData>({
    email: user?.email || '',
    password: '',
    username: user?.username || '',
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    is_active: user?.is_active ?? true,
    is_superuser: user?.is_superuser ?? false,
    is_verified: user?.is_verified ?? false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (user) {
      // Обновление пользователя
      const submitData: UserUpdate = {
        email: formData.email || null,
        username: formData.username || null,
        first_name: formData.first_name || null,
        last_name: formData.last_name || null,
        is_active: formData.is_active,
        is_superuser: formData.is_superuser,
        is_verified: formData.is_verified,
        ...(formData.password ? { password: formData.password } : {}),
      };
      onSubmit(submitData);
    } else {
      // Создание пользователя
      const submitData: UserCreate = {
        email: formData.email,
        password: formData.password,
        username: formData.username,
        first_name: formData.first_name || null,
        last_name: formData.last_name || null,
        is_active: formData.is_active,
        is_superuser: formData.is_superuser,
        is_verified: formData.is_verified,
      };
      onSubmit(submitData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="username">Имя пользователя</Label>
          <Input
            id="username"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            required
          />
        </div>
      </div>

      {!user && (
        <div className="space-y-2">
          <Label htmlFor="password">Пароль</Label>
          <Input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            required={!user}
            minLength={8}
          />
        </div>
      )}

      {user && (
        <div className="space-y-2">
          <Label htmlFor="password">Новый пароль (оставьте пустым, чтобы не менять)</Label>
          <Input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            minLength={8}
          />
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="first_name">Имя</Label>
          <Input
            id="first_name"
            value={formData.first_name}
            onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="last_name">Фамилия</Label>
          <Input
            id="last_name"
            value={formData.last_name}
            onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
          />
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center space-x-2">
          <Checkbox
            id="is_active"
            checked={formData.is_active}
            onCheckedChange={(checked) => 
              setFormData({ ...formData, is_active: checked as boolean })
            }
          />
          <Label htmlFor="is_active" className="cursor-pointer">
            Активный пользователь
          </Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="is_superuser"
            checked={formData.is_superuser}
            onCheckedChange={(checked) => 
              setFormData({ ...formData, is_superuser: checked as boolean })
            }
          />
          <Label htmlFor="is_superuser" className="cursor-pointer">
            Суперпользователь
          </Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="is_verified"
            checked={formData.is_verified}
            onCheckedChange={(checked) => 
              setFormData({ ...formData, is_verified: checked as boolean })
            }
          />
          <Label htmlFor="is_verified" className="cursor-pointer">
            Email подтвержден
          </Label>
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

