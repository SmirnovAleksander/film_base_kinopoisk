import { FilmWithDetails } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import FilmForm from '@/components/admin/forms/FilmForm';
import { Calendar, Clock, Edit, Film, Plus, Star, Trash2 } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';

type EditingFilmState = FilmWithDetails | null | undefined;

interface FilmsSectionProps {
  films: FilmWithDetails[] | null;
  editingFilm: EditingFilmState;
  setEditingFilm: Dispatch<SetStateAction<EditingFilmState>>;
  onSubmit: (filmData: any) => Promise<void>;
  onDelete: (filmId: number) => Promise<void>;
}

const formatRating = (rating: number | null | undefined) => {
  return rating ? rating.toFixed(1) : '-';
};

const formatYear = (year: number | null | undefined) => {
  return year || '-';
};

const formatDuration = (duration: string | null | undefined) => {
  return duration || '-';
};

export default function FilmsSection({
  films,
  editingFilm,
  setEditingFilm,
  onSubmit,
  onDelete,
}: FilmsSectionProps) {
  if (editingFilm !== undefined) {
    const isCreating = editingFilm === null;
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Film className="h-5 w-5" />
              {isCreating ? 'Добавить фильм' : 'Редактировать фильм'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea>
            <FilmForm
              film={isCreating ? null : editingFilm}
              onSubmit={onSubmit}
              onCancel={() => setEditingFilm(undefined)}
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
            <Film className="h-5 w-5" />
            Управление фильмами
          </CardTitle>
          <Button onClick={() => setEditingFilm(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить фильм
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
                <TableHead>Название</TableHead>
                <TableHead>Оригинальное название</TableHead>
                <TableHead>Год</TableHead>
                <TableHead>Жанры</TableHead>
                <TableHead>Страны</TableHead>
                <TableHead>Рейтинг КП</TableHead>
                <TableHead>Рейтинг IMDb</TableHead>
                <TableHead>Длительность</TableHead>
                <TableHead>Премьера</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {films?.map((film) => (
                <TableRow key={film.id}>
                  <TableCell className="font-mono text-sm">
                    {film.id}
                  </TableCell>
                  <TableCell className="font-mono text-sm">
                    {film.kinopoisk_id}
                  </TableCell>
                  <TableCell className="font-medium max-w-[200px]">
                    <div className="truncate" title={film.title || ''}>
                      {film.title || '-'}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[200px]">
                    <div className="truncate" title={film.original_title || ''}>
                      {film.original_title || '-'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">
                      {formatYear(film.year)}
                    </Badge>
                  </TableCell>
                  <TableCell className="max-w-[150px]">
                    <div className="flex flex-wrap gap-1">
                      {film.genres?.slice(0, 2).map((genre) => (
                        <Badge key={genre.id} variant="outline" className="text-xs">
                          {genre.name}
                        </Badge>
                      ))}
                      {film.genres && film.genres.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{film.genres.length - 2}
                        </Badge>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-[120px]">
                    <div className="flex flex-wrap gap-1">
                      {film.countries?.slice(0, 2).map((country) => (
                        <Badge key={country.id} variant="outline" className="text-xs">
                          {country.name}
                        </Badge>
                      ))}
                      {film.countries && film.countries.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{film.countries.length - 2}
                        </Badge>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Star className="h-3 w-3 text-yellow-500" />
                      {formatRating(film.rating_kp)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Star className="h-3 w-3 text-blue-500" />
                      {formatRating(film.rating_imdb)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3 text-gray-500" />
                      {formatDuration(film.duration)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3 w-3 text-gray-500" />
                      {film.ru_premiere || '-'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditingFilm(film)}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => onDelete(film.id)}
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

