import { Media } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import MediaForm from '@/components/admin/MediaForm';
import { Calendar, Edit, Newspaper, Plus, Trash2 } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';

type EditingMediaState = Media | null | undefined;

interface MediaSectionProps {
  media: Media[] | null;
  editingMedia: EditingMediaState;
  setEditingMedia: Dispatch<SetStateAction<EditingMediaState>>;
  onSubmit: (mediaData: any) => Promise<void>;
  onDelete: (mediaId: number) => Promise<void>;
}

export default function MediaSection({
  media,
  editingMedia,
  setEditingMedia,
  onSubmit,
  onDelete,
}: MediaSectionProps) {
  if (editingMedia !== undefined) {
    const isCreating = editingMedia === null;
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Newspaper className="h-5 w-5" />
              {isCreating ? 'Добавить медиа' : 'Редактировать медиа'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea>
            <MediaForm
              media={isCreating ? null : editingMedia}
              onSubmit={onSubmit}
              onCancel={() => setEditingMedia(undefined)}
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
            <Newspaper className="h-5 w-5" />
            Управление медиа
          </CardTitle>
          <Button onClick={() => setEditingMedia(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить медиа
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[600px]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Тип</TableHead>
                <TableHead>Заголовок</TableHead>
                <TableHead>Категория</TableHead>
                <TableHead>Тип карточки</TableHead>
                <TableHead>Дата</TableHead>
                <TableHead>URL</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {media?.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-mono text-sm">
                    {item.id}
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">
                      {item.type || '-'}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium max-w-[200px]">
                    <div className="truncate" title={item.title || ''}>
                      {item.title || '-'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">
                      {item.category || '-'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {item.card_type || '-'}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3 text-gray-500" />
                      {item.date || '-'}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[150px]">
                    <div className="truncate" title={item.url || ''}>
                      {item.url ? (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 hover:underline"
                        >
                          {item.url}
                        </a>
                      ) : '-'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditingMedia(item)}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => onDelete(item.id)}
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

