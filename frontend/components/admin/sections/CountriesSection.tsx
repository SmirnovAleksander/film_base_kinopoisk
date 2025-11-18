import { Country } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import CountryForm from '@/components/admin/CountryForm';
import { Edit, Globe, Plus, Trash2 } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';

type EditingCountryState = Country | null | undefined;

interface CountriesSectionProps {
  countries: Country[] | null;
  editingCountry: EditingCountryState;
  setEditingCountry: Dispatch<SetStateAction<EditingCountryState>>;
  onSubmit: (countryData: any) => Promise<void>;
  onDelete: (countryId: number) => Promise<void>;
}

export default function CountriesSection({
  countries,
  editingCountry,
  setEditingCountry,
  onSubmit,
  onDelete,
}: CountriesSectionProps) {
  if (editingCountry !== undefined) {
    const isCreating = editingCountry === null;
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5" />
              {isCreating ? 'Добавить страну' : 'Редактировать страну'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <ScrollArea>
            <CountryForm
              country={isCreating ? null : editingCountry}
              onSubmit={onSubmit}
              onCancel={() => setEditingCountry(undefined)}
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
            <Globe className="h-5 w-5" />
            Управление странами
          </CardTitle>
          <Button onClick={() => setEditingCountry(null)}>
            <Plus className="h-4 w-4 mr-2" />
            Добавить страну
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
              {countries?.map((country) => (
                <TableRow key={country.id}>
                  <TableCell className="font-mono text-sm">
                    {country.id}
                  </TableCell>
                  <TableCell className="font-medium">
                    <Badge variant="outline" className="text-sm">
                      {country.name}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditingCountry(country)}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => onDelete(country.id)}
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

