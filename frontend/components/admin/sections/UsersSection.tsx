import { User } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import UserForm from '@/components/admin/forms/UserForm';
import { Calendar, Edit, Plus, Trash2, UserCog } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';

type EditingUserState = User | null | undefined;

interface UsersSectionProps {
  users: User[] | null;
  editingUser: EditingUserState;
  setEditingUser: Dispatch<SetStateAction<EditingUserState>>;
  onSubmit: (userData: any) => Promise<void>;
  onDelete: (userId: number) => Promise<void>;
}

export default function UsersSection({
  users,
  editingUser,
  setEditingUser,
  onSubmit,
  onDelete,
}: UsersSectionProps) {
  if (editingUser !== undefined) {
    const isCreating = editingUser === null;
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <UserCog className="h-5 w-5" />
              {isCreating ? 'Добавить пользователя' : 'Редактировать пользователя'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea>
            <UserForm
              user={isCreating ? null : editingUser}
              onSubmit={onSubmit}
              onCancel={() => setEditingUser(undefined)}
            />
          </ScrollArea>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <UserCog className="h-5 w-5" />
            Управление пользователями
          </CardTitle>
          <Button onClick={() => setEditingUser(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить пользователя
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[600px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Имя пользователя</TableHead>
                <TableHead>Имя</TableHead>
                <TableHead>Фамилия</TableHead>
                <TableHead>Активен</TableHead>
                <TableHead>Суперпользователь</TableHead>
                <TableHead>Подтвержден</TableHead>
                <TableHead>Дата создания</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users?.map((user) => (
                <TableRow key={user.id}>
                  <TableCell className="font-mono text-sm">
                    {user.id}
                  </TableCell>
                  <TableCell className="font-medium">
                    {user.email}
                  </TableCell>
                  <TableCell>
                    {user.username}
                  </TableCell>
                  <TableCell>
                    {user.first_name || '-'}
                  </TableCell>
                  <TableCell>
                    {user.last_name || '-'}
                  </TableCell>
                  <TableCell>
                    <Badge variant={user.is_active ? 'default' : 'secondary'}>
                      {user.is_active ? 'Да' : 'Нет'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={user.is_superuser ? 'destructive' : 'outline'}>
                      {user.is_superuser ? 'Да' : 'Нет'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={user.is_verified ? 'default' : 'secondary'}>
                      {user.is_verified ? 'Да' : 'Нет'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3 text-gray-500" />
                      {new Date(user.created_at).toLocaleDateString('ru-RU')}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditingUser(user)}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => onDelete(user.id)}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}

