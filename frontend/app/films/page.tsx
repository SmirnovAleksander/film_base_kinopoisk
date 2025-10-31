'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Filter, Search, SortAsc, SortDesc } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';
import { FilmCard, FilmCardSkeleton } from '@/components/film';
import { useFilmsStore } from '@/store';
import { FilmFilterParams } from '@/lib/types';

export default function FilmsPage() {
  const searchParams = useSearchParams();
  const {
    films,
    genres,
    countries,
    searchQuery,
    filters,
    isLoading,
    isSearching,
    currentPage,
    pageSize,
    totalCount,
    searchFilms,
    filterFilms,
    fetchGenres,
    fetchCountries,
    setSearchQuery,
    setFilters,
    setPage,
  } = useFilmsStore();

  const [localSearchQuery, setLocalSearchQuery] = useState('');
  const [localFilters, setLocalFilters] = useState<FilmFilterParams>({});
  const [sortBy, setSortBy] = useState<'title' | 'year' | 'rating'>('title');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [showFilters, setShowFilters] = useState(false);
  
  // Значения для слайдеров
  const currentYear = new Date().getFullYear();
  const [yearRange, setYearRange] = useState<[number, number]>([1890, currentYear]);
  const [ratingRange, setRatingRange] = useState<[number, number]>([1, 10]);

  // Инициализация данных
  useEffect(() => {
    fetchGenres();
    fetchCountries();
  }, [fetchGenres, fetchCountries]);

  // Обработка URL параметров при загрузке
  useEffect(() => {
    const search = searchParams.get('search');
    const genre = searchParams.get('genre');
    const country = searchParams.get('country');
    const startYear = searchParams.get('start_year');
    const endYear = searchParams.get('end_year');
    const minRating = searchParams.get('min_rating');
    const maxRating = searchParams.get('max_rating');

    if (search) {
      handleSearch(search);
    } else {
      // Загружаем все фильмы
      filterFilms({ page: 1, page_size: pageSize });
    }

    // Применяем фильтры из URL
    if (genre || country || startYear || endYear || minRating || maxRating) {
      const filterParams: FilmFilterParams = {
        page: 1,
        page_size: pageSize,
        genre_id: genre ? parseInt(genre) : undefined,
        country_id: country ? parseInt(country) : undefined,
        start_year: startYear ? parseInt(startYear) : undefined,
        end_year: endYear ? parseInt(endYear) : undefined,
        min_rating: minRating ? parseFloat(minRating) : undefined,
        max_rating: maxRating ? parseFloat(maxRating) : undefined,
      };
      filterFilms(filterParams);
      
      // Обновляем слайдеры если есть значения в URL
      if (startYear || endYear) {
        setYearRange([
          startYear ? parseInt(startYear) : 1890,
          endYear ? parseInt(endYear) : currentYear
        ]);
      }
      if (minRating || maxRating) {
        setRatingRange([
          minRating ? parseFloat(minRating) : 1,
          maxRating ? parseFloat(maxRating) : 10
        ]);
      }
    }
  }, [searchParams, currentYear]);

  const handleSearch = async (query?: string) => {
    const searchTerm = query || localSearchQuery;
    if (!searchTerm.trim()) return;

    setSearchQuery(searchTerm);
    await searchFilms({
      query: searchTerm.trim(),
      page: 1,
      page_size: pageSize,
    });
  };

  const handleFilterApply = async () => {
    const filterParams: FilmFilterParams = {
      ...localFilters,
      page: 1,
      page_size: pageSize,
      start_year: yearRange[0],
      end_year: yearRange[1],
      min_rating: ratingRange[0],
      max_rating: ratingRange[1],
    };

    setFilters(filterParams);
    await filterFilms(filterParams);
    setShowFilters(false);
  };

  const handleFilterReset = () => {
    setLocalFilters({});
    setSearchQuery('');
    setLocalSearchQuery('');
    setYearRange([1890, currentYear]);
    setRatingRange([1, 10]);
    filterFilms({ page: 1, page_size: pageSize });
  };

  const handlePageChange = async (page: number) => {
    setPage(page);
    if (searchQuery) {
      await searchFilms({
        query: searchQuery,
        page,
        page_size: pageSize,
      });
    } else if (Object.keys(filters).length > 0) {
      await filterFilms({ ...filters, page });
    } else {
      await filterFilms({ page, page_size: pageSize });
    }
  };

  // Обработчики для слайдеров
  const handleYearRangeChange = (value: number[]) => {
    setYearRange([value[0], value[1]]);
  };

  const handleRatingRangeChange = (value: number[]) => {
    setRatingRange([value[0], value[1]]);
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Каталог фильмов</h1>
        <p className="text-muted-foreground">
          Найдено фильмов: {totalCount}
        </p>
      </div>

      {/* Поиск и фильтры */}
      <div className="mb-8 space-y-4">
        {/* Поиск */}
        <div className="flex gap-2">
          <div className="flex-1">
            <Input
              placeholder="Поиск фильмов..."
              value={localSearchQuery}
              onChange={(e) => setLocalSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="w-full"
            />
          </div>
          <Button onClick={() => handleSearch()} disabled={!localSearchQuery.trim()}>
            <Search className="h-4 w-4 mr-2" />
            Поиск
          </Button>
          <Button 
            variant="outline" 
            onClick={() => setShowFilters(!showFilters)}
            className={showFilters ? 'bg-accent' : ''}
          >
            <Filter className="h-4 w-4 mr-2" />
            Фильтры
          </Button>
        </div>

        {/* Панель фильтров */}
        {showFilters && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Фильтры</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Жанр */}
                <div className="space-y-2">
                  <Label htmlFor="genre">Жанр</Label>
                  <Select
                    value={localFilters.genre_id?.toString() || 'all'}
                    onValueChange={(value) =>
                      setLocalFilters(prev => ({
                        ...prev,
                        genre_id: value === 'all' ? undefined : parseInt(value)
                      }))
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Выберите жанр" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Все жанры</SelectItem>
                      {genres.map((genre) => (
                        <SelectItem key={genre.id} value={genre.id.toString()}>
                          {genre.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Страна */}
                <div className="space-y-2">
                  <Label htmlFor="country">Страна</Label>
                  <Select
                    value={localFilters.country_id?.toString() || 'all'}
                    onValueChange={(value) =>
                      setLocalFilters(prev => ({
                        ...prev,
                        country_id: value === 'all' ? undefined : parseInt(value)
                      }))
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Выберите страну" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Все страны</SelectItem>
                      {countries.map((country) => (
                        <SelectItem key={country.id} value={country.id.toString()}>
                          {country.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Год выпуска */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label>Год выпуска</Label>
                    <div className="flex gap-2 text-sm text-muted-foreground">
                      <span>{yearRange[0]}</span>
                      <span>-</span>
                      <span>{yearRange[1]}</span>
                    </div>
                  </div>
                  <Slider
                    min={1890}
                    max={currentYear}
                    step={1}
                    value={yearRange}
                    onValueChange={handleYearRangeChange}
                    className="w-full"
                  />
                  <div className="flex gap-2">
                    <Input
                      placeholder="С"
                      type="number"
                      min="1890"
                      max={currentYear.toString()}
                      value={yearRange[0]}
                      onChange={(e) => {
                        const value = parseInt(e.target.value) || 1890;
                        const newRange: [number, number] = [Math.min(value, yearRange[1]), yearRange[1]];
                        setYearRange(newRange);
                      }}
                    />
                    <Input
                      placeholder="По"
                      type="number"
                      min="1890"
                      max={currentYear.toString()}
                      value={yearRange[1]}
                      onChange={(e) => {
                        const value = parseInt(e.target.value) || currentYear;
                        const newRange: [number, number] = [yearRange[0], Math.max(value, yearRange[0])];
                        setYearRange(newRange);
                      }}
                    />
                  </div>
                </div>

                {/* Рейтинг */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label>Рейтинг</Label>
                    <div className="flex gap-2 text-sm text-muted-foreground">
                      <span>{ratingRange[0]}</span>
                      <span>-</span>
                      <span>{ratingRange[1]}</span>
                    </div>
                  </div>
                  <Slider
                    min={1}
                    max={10}
                    step={0.1}
                    value={ratingRange}
                    onValueChange={handleRatingRangeChange}
                    className="w-full"
                  />
                  <div className="flex gap-2">
                    <Input
                      placeholder="Мин"
                      type="number"
                      min="1"
                      max="10"
                      step="0.1"
                      value={ratingRange[0]}
                      onChange={(e) => {
                        const value = parseFloat(e.target.value) || 1;
                        const newRange: [number, number] = [Math.min(value, ratingRange[1]), ratingRange[1]];
                        setRatingRange(newRange);
                      }}
                    />
                    <Input
                      placeholder="Макс"
                      type="number"
                      min="1"
                      max="10"
                      step="0.1"
                      value={ratingRange[1]}
                      onChange={(e) => {
                        const value = parseFloat(e.target.value) || 10;
                        const newRange: [number, number] = [ratingRange[0], Math.max(value, ratingRange[0])];
                        setRatingRange(newRange);
                      }}
                    />
                  </div>
                </div>
              </div>

              <div className="flex gap-2 pt-4">
                <Button onClick={handleFilterApply}>
                  Применить фильтры
                </Button>
                <Button variant="outline" onClick={handleFilterReset}>
                  Сбросить
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Активные фильтры */}
        {(searchQuery || Object.keys(filters).length > 0) && (
          <div className="flex flex-wrap gap-2 items-center">
            <span className="text-sm text-muted-foreground">Активные фильтры:</span>
            
            {searchQuery && (
              <Badge variant="secondary" className="flex items-center gap-1">
                Поиск: {searchQuery}
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-auto p-0 ml-1"
                  onClick={() => {
                    setSearchQuery('');
                    setLocalSearchQuery('');
                    filterFilms({ page: 1, page_size: pageSize });
                  }}
                >
                  ×
                </Button>
              </Badge>
            )}
            
            {filters.genre_id && (
              <Badge variant="secondary" className="flex items-center gap-1">
                Жанр: {genres.find(g => g.id === filters.genre_id)?.name}
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-auto p-0 ml-1"
                  onClick={() => {
                    setFilters({ ...filters, genre_id: undefined });
                    filterFilms({ ...filters, genre_id: undefined, page: 1 });
                  }}
                >
                  ×
                </Button>
              </Badge>
            )}

            {/* Другие фильтры */}
            {(filters.start_year || filters.end_year || filters.min_rating || filters.max_rating) && (
              <div className="flex items-center gap-2">
                {/* Год выпуска (скрываем если дефолтные значения) */}
                {(filters.start_year || filters.end_year) &&
                 !(filters.start_year === 1890 && filters.end_year === currentYear) && (
                  <Badge variant="secondary" className="flex items-center gap-1">
                    Год: {filters.start_year}-{filters.end_year}
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-auto p-0 ml-1"
                      onClick={() => {
                        setYearRange([1890, currentYear]);
                        const newFilters = { ...filters };
                        delete newFilters.start_year;
                        delete newFilters.end_year;
                        setFilters(newFilters);
                        filterFilms({ ...newFilters, page: 1 });
                      }}
                    >
                      ×
                    </Button>
                  </Badge>
                )}
                
                {/* Рейтинг (скрываем если дефолтные значения) */}
                {(filters.min_rating || filters.max_rating) &&
                 !(filters.min_rating === 1 && filters.max_rating === 10) && (
                  <Badge variant="secondary" className="flex items-center gap-1">
                    Рейтинг: {filters.min_rating}-{filters.max_rating}
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-auto p-0 ml-1"
                      onClick={() => {
                        setRatingRange([1, 10]);
                        const newFilters = { ...filters };
                        delete newFilters.min_rating;
                        delete newFilters.max_rating;
                        setFilters(newFilters);
                        filterFilms({ ...newFilters, page: 1 });
                      }}
                    >
                      ×
                    </Button>
                  </Badge>
                )}
              </div>
            )}

            <Button
              variant="ghost"
              size="sm"
              onClick={handleFilterReset}
              className="text-muted-foreground"
            >
              Очистить все
            </Button>
          </div>
        )}
      </div>

      {/* Список фильмов */}
      <div className="space-y-6">
        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
            {Array.from({ length: 12 }).map((_, i) => (
              <FilmCardSkeleton key={i} />
            ))}
          </div>
        ) : films.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {films.map((film) => (
                <FilmCard key={film.id} film={film} />
              ))}
            </div>

            {/* Пагинация */}
            {totalPages > 1 && (
              <Pagination>
                <PaginationContent>
                  <PaginationItem>
                    <PaginationPrevious
                      href="#"
                      onClick={(e: React.MouseEvent) => {
                        e.preventDefault();
                        if (currentPage > 1) {
                          handlePageChange(currentPage - 1);
                        }
                      }}
                    />
                  </PaginationItem>
                  
                  {(() => {
                    const pageNumbers = [];
                    const showPages = Math.min(7, totalPages);
                    
                    if (totalPages <= showPages) {
                      // Показываем все страницы если их мало
                      for (let i = 1; i <= totalPages; i++) {
                        pageNumbers.push(
                          <PaginationItem key={i}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === i}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(i);
                              }}
                            >
                              {i}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      }
                    } else {
                      // Сложная логика для большого количества страниц
                      const startPage = Math.max(1, currentPage - 2);
                      const endPage = Math.min(totalPages, currentPage + 2);
                      
                      // Первая страница
                      if (startPage > 1) {
                        pageNumbers.push(
                          <PaginationItem key={1}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === 1}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(1);
                              }}
                            >
                              1
                            </PaginationLink>
                          </PaginationItem>
                        );
                        
                        if (startPage > 2) {
                          pageNumbers.push(<PaginationEllipsis key="ellipsis-start" />);
                        }
                      }
                      
                      // Страницы вокруг текущей
                      for (let i = startPage; i <= endPage; i++) {
                        pageNumbers.push(
                          <PaginationItem key={i}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === i}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(i);
                              }}
                            >
                              {i}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      }
                      
                      // Последняя страница
                      if (endPage < totalPages) {
                        if (endPage < totalPages - 1) {
                          pageNumbers.push(<PaginationEllipsis key="ellipsis-end" />);
                        }
                        
                        pageNumbers.push(
                          <PaginationItem key={totalPages}>
                            <PaginationLink
                              href="#"
                              isActive={currentPage === totalPages}
                              onClick={(e: React.MouseEvent) => {
                                e.preventDefault();
                                handlePageChange(totalPages);
                              }}
                            >
                              {totalPages}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      }
                    }
                    
                    return pageNumbers;
                  })()}
                  
                  <PaginationItem>
                    <PaginationNext
                      href="#"
                      onClick={(e: React.MouseEvent) => {
                        e.preventDefault();
                        if (currentPage < totalPages) {
                          handlePageChange(currentPage + 1);
                        }
                      }}
                    />
                  </PaginationItem>
                </PaginationContent>
              </Pagination>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">
              {isSearching ? 'Поиск не дал результатов' : 'Фильмы не найдены'}
            </p>
            <p className="text-muted-foreground mt-2">
              Попробуйте изменить параметры поиска или фильтры
            </p>
          </div>
        )}
      </div>
    </div>
  );
}