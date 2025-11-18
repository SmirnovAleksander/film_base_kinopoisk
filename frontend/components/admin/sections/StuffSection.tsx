import { Stuff } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import StuffForm from '@/components/admin/forms/StuffForm';
import { Calendar, Edit, Film, Plus, Trash2, Users } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';

interface StuffResponse {
  items: Stuff[];
  page: number;
  page_size: number;
  total_count: number;
}

type EditingStuffState = Stuff | null | undefined;

interface StuffSectionProps {
  stuff: StuffResponse | null;
  editingStuff: EditingStuffState;
  setEditingStuff: Dispatch<SetStateAction<EditingStuffState>>;
  onSubmit: (stuffData: any) => Promise<void>;
  onDelete: (stuffId: number) => Promise<void>;
}

const formatArrayField = (field: string[] | null | undefined) => {
  if (!field || field.length === 0) return '-';
  return field.join(', ');
};

export default function StuffSection({
  stuff,
  editingStuff,
  setEditingStuff,
  onSubmit,
  onDelete,
}: StuffSectionProps) {
  if (editingStuff !== undefined) {
    const isCreating = editingStuff === null;
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              {isCreating ? 'Добавить участника' : 'Редактировать участника'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea>
            <StuffForm
              stuff={isCreating ? null : editingStuff}
              onSubmit={onSubmit}
              onCancel={() => setEditingStuff(undefined)}
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
            <Users className="h-5 w-5" />
            Управление участниками
          </CardTitle>
          <Button onClick={() => setEditingStuff(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить участника
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[600px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>kpID</TableHead>
                <TableHead>Имя</TableHead>
                <TableHead>Оригинальное имя</TableHead>
                <TableHead>Карьера</TableHead>
                <TableHead>Жанры</TableHead>
                <TableHead>Возраст</TableHead>
                <TableHead>Год рождения</TableHead>
                <TableHead>Место рождения</TableHead>
                <TableHead>Фильмов</TableHead>
                <TableHead>Рост</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {stuff?.items?.map((person) => (
                <TableRow key={person.id}>
                  <TableCell className="font-mono text-sm">
                    {person.id}
                  </TableCell>
                  <TableCell className="font-mono text-sm">
                    {person.kinopoisk_id}
                  </TableCell>
                  <TableCell className="font-medium max-w-[150px]">
                    <div className="truncate" title={person.name || ''}>
                      {person.name || '-'}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[150px]">
                    <div className="truncate" title={person.original_name || ''}>
                      {person.original_name || '-'}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[120px]">
                    <div className="flex flex-wrap gap-1">
                      {person.career?.slice(0, 2).map((career, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {career}
                        </Badge>
                      ))}
                      {person.career && person.career.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{person.career.length - 2}
                        </Badge>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[100px]">
                    <div className="flex flex-wrap gap-1">
                      {person.ganres?.slice(0, 2).map((genre, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {genre}
                        </Badge>
                      ))}
                      {person.ganres && person.ganres.length > 2 && (
                        <Badge variant="secondary" className="text-xs">
                          +{person.ganres.length - 2}
                        </Badge>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">
                      {person.age || '-'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3 text-gray-500" />
                      {person.birthday_day_month || '-'}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[100px]">
                    <div className="truncate" title={formatArrayField(person.birthplace)}>
                      {formatArrayField(person.birthplace)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Film className="h-3 w-3 text-gray-500" />
                      {person.total_films || '-'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">
                      {person.height || '-'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditingStuff(person)}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => onDelete(person.id)}
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

