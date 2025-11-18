import { Genre } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import GenreForm from '@/components/admin/GenreForm';
import { Edit, Plus, Tag, Trash2 } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';

type EditingGenreState = Genre | null | undefined;

interface GenresSectionProps {
  genres: Genre[] | null;
  editingGenre: EditingGenreState;
  setEditingGenre: Dispatch<SetStateAction<EditingGenreState>>;
  onSubmit: (genreData: any) => Promise<void>;
  onDelete: (genreId: number) => Promise<void>;
}

export default function GenresSection({
  genres,
  editingGenre,
  setEditingGenre,
  onSubmit,
  onDelete,
}: GenresSectionProps) {
  if (editingGenre !== undefined) {
    const isCreating = editingGenre === null;
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Tag className="h-5 w-5" />
              {isCreating ? 'Добавить жанр' : 'Редактировать жанр'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea>
            <GenreForm
              genre={isCreating ? null : editingGenre}
              onSubmit={onSubmit}
              onCancel={() => setEditingGenre(undefined)}
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
            <Tag className="h-5 w-5" />
            Управление жанрами
          </CardTitle>
          <Button onClick={() => setEditingGenre(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить жанр
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[600px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Название</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {genres?.map((genre) => (
                <TableRow key={genre.id}>
                  <TableCell className="font-mono text-sm">
                    {genre.id}
                  </TableCell>
                  <TableCell className="font-medium">
                    <Badge variant="outline" className="text-sm">
                      {genre.name}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditingGenre(genre)}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => onDelete(genre.id)}
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

