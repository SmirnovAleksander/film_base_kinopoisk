'use client';

import { useState } from 'react';
import { useFilmsStore } from '@/store';
import { Film, FilmSearchParams, FilmFilterParams } from '@/lib/types';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Search, Filter, Film as FilmIcon } from 'lucide-react';

export function FilmsPage() {
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(20);
  const [searchParams, setSearchParams] = useState<FilmSearchParams | null>(null);
  const [filterParams, setFilterParams] = useState<FilmFilterParams | null>(null);
  const [activeTab, setActiveTab] = useState('all');

  // Store состояние
  const {
    films,
    isLoading: filmsLoading,
    totalCount,
    fetchFilms,
    searchFilms: searchFilmsAction,
    filterFilms: filterFilmsAction,
  } = useFilmsStore();

  const { user: currentUser } = useAuth();

  const handleSearch = (query: string, lang: string = 'ru') => {
    if (query.trim()) {
      setSearchParams({ query, lang, page: 1 });
      setCurrentPage(1);
      setActiveTab('search');
      searchFilmsAction({ query, lang, page: 1, page_size: pageSize });
    }
  };

  const handleFilter = (params: Partial<FilmFilterParams>) => {
    const newParams = { ...params, page: 1, page_size: pageSize };
    setFilterParams(newParams);
    setCurrentPage(1);
    setActiveTab('filter');
    filterFilmsAction(newParams);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    
    if (activeTab === 'search' && searchParams) {
      const newParams = { ...searchParams, page, page_size: pageSize };
      searchFilmsAction(newParams);
    } else if (activeTab === 'filter' && filterParams) {
      const newParams = { ...filterParams, page, page_size: pageSize };
      filterFilmsAction(newParams);
    } else {
      fetchFilms(page);
    }
  };

  const FilmComponent = ({ film }: { film: Film }) => {
    return (
      <Card className="p-4">
        <div className="flex gap-4">
          <img 
            src={film.poster || '/placeholder.jpg'} 
            alt={film.title || 'Без названия'} 
            className="w-24 h-36 object-cover rounded"
          />
          <div className="flex-1">
            <h3 className="text-lg font-semibold">{film.title}</h3>
            <p className="text-sm text-muted-foreground">{film.original_title}</p>
            <p className="text-sm mt-2 line-clamp-2">{film.description}</p>
            
            <div className="flex items-center gap-2 mt-2">
              {film.rating_kp && (
                <span className="text-sm font-medium">
                  КП: {film.rating_kp}
                </span>
              )}
              {film.year && (
                <span className="text-sm text-muted-foreground">
                  {film.year}
                </span>
              )}
            </div>
          </div>
        </div>
      </Card>
    );
  };

  // Убрал обработку ошибок, так как в store нет поля error

  const currentData = {
    items: films,
    total_count: totalCount,
  };

  return (
    <div className="container mx-auto p-4 space-y-6">
      {/* Заголовок */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Фильмы</h1>
        
        {currentUser ? (
          <div className="flex items-center gap-4">
            <span>Привет, {currentUser.email}</span>
          </div>
        ) : (
          <span className="text-muted-foreground">Войдите для персонализации</span>
        )}
      </div>

      {/* Вкладки */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="all">Все фильмы</TabsTrigger>
          <TabsTrigger value="search">Поиск</TabsTrigger>
          <TabsTrigger value="filter">Фильтры</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {/* Список всех фильмов */}
          {filmsLoading ? (
            <div className="grid gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <Skeleton key={i} className="h-32 w-full" />
              ))}
            </div>
          ) : (
            <>
              <div className="grid gap-4">
                {currentData.items?.map((film) => (
                  <FilmComponent key={film.id} film={film} />
                ))}
              </div>
              
              {/* Пагинация */}
              {currentData && currentData.total_count > pageSize && (
                <Pagination
                  currentPage={currentPage}
                  totalPages={Math.ceil(currentData.total_count / pageSize)}
                  onPageChange={handlePageChange}
                />
              )}
            </>
          )}
        </TabsContent>

        <TabsContent value="search" className="space-y-4">
          {/* Поиск */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Search className="w-5 h-5" />
                Поиск фильмов
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Введите название фильма..."
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      handleSearch((e.target as HTMLInputElement).value);
                    }
                  }}
                />
                <Select defaultValue="ru">
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ru">Русское</SelectItem>
                    <SelectItem value="en">Оригинальное</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Результаты поиска */}
          {filmsLoading ? (
            <div className="grid gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <Skeleton key={i} className="h-32 w-full" />
              ))}
            </div>
          ) : (
            <div className="grid gap-4">
              {currentData.items?.map((film) => (
                <FilmComponent key={film.id} film={film} />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="filter" className="space-y-4">
          {/* Фильтры */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Filter className="w-5 h-5" />
                Фильтры
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Input
                  placeholder="Название фильма"
                  onChange={(e) => handleFilter({ title: e.target.value })}
                />
                <Input
                  placeholder="Начальный год"
                  type="number"
                  onChange={(e) => handleFilter({ start_year: parseInt(e.target.value) || undefined })}
                />
                <Input
                  placeholder="Конечный год"
                  type="number"
                  onChange={(e) => handleFilter({ end_year: parseInt(e.target.value) || undefined })}
                />
              </div>
            </CardContent>
          </Card>

          {/* Результаты фильтрации */}
          {filmsLoading ? (
            <div className="grid gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <Skeleton key={i} className="h-32 w-full" />
              ))}
            </div>
          ) : (
            <div className="grid gap-4">
              {currentData.items?.map((film) => (
                <FilmComponent key={film.id} film={film} />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

// Компонент пагинации
function Pagination({ 
  currentPage, 
  totalPages, 
  onPageChange 
}: { 
  currentPage: number; 
  totalPages: number; 
  onPageChange: (page: number) => void; 
}) {
  return (
    <div className="flex justify-center gap-2">
      <Button
        variant="outline"
        size="sm"
        disabled={currentPage <= 1}
        onClick={() => onPageChange(currentPage - 1)}
      >
        Предыдущая
      </Button>
      
      <span className="px-4 py-2 text-sm">
        Страница {currentPage} из {totalPages}
      </span>
      
      <Button
        variant="outline"
        size="sm"
        disabled={currentPage >= totalPages}
        onClick={() => onPageChange(currentPage + 1)}
      >
        Следующая
      </Button>
    </div>
  );
}