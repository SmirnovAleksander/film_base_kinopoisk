'use client';

import { useState, useEffect } from 'react';
import { Filter, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { Genre, Country, FilmFilterParams } from '@/lib/types';

interface FilmsFiltersProps {
  genres: Genre[];
  countries: Country[];
  searchQuery: string;
  filters: FilmFilterParams;
  totalCount: number;
  
  isLoading: boolean;
  isSearching: boolean;
  
  onSearch: (query: string) => Promise<void>;
  onFilterApply: (filters: FilmFilterParams) => Promise<void>;
  onFilterReset: () => void;
  onFilterRemove: (key: keyof FilmFilterParams) => void;
  
  pageSize: number;
}

export function FilmsFilters({
  genres,
  countries,
  searchQuery,
  filters,
  totalCount,
  isLoading,
  isSearching,
  onSearch,
  onFilterApply,
  onFilterReset,
  onFilterRemove,
  pageSize,
}: FilmsFiltersProps) {
  const [localSearchQuery, setLocalSearchQuery] = useState('');
  const [localFilters, setLocalFilters] = useState<FilmFilterParams>({});
  const [showFilters, setShowFilters] = useState(false);
  
  const currentYear = new Date().getFullYear();
  const [yearRange, setYearRange] = useState<[number, number]>([1890, currentYear]);
  const [ratingRange, setRatingRange] = useState<[number, number]>([1, 10]);

  useEffect(() => {
    setLocalSearchQuery(searchQuery);
    setLocalFilters(filters);
    
    if (filters.start_year || filters.end_year) {
      setYearRange([
        filters.start_year || 1890,
        filters.end_year || currentYear
      ]);
    }
    if (filters.min_rating || filters.max_rating) {
      setRatingRange([
        filters.min_rating || 1,
        filters.max_rating || 10
      ]);
    }
  }, [searchQuery, filters, currentYear]);

  const handleSearch = async () => {
    if (!localSearchQuery.trim()) return;
    await onSearch(localSearchQuery.trim());
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

    await onFilterApply(filterParams);
    setShowFilters(false);
  };

  const handleFilterReset = () => {
    setLocalFilters({});
    setLocalSearchQuery('');
    setYearRange([1890, currentYear]);
    setRatingRange([1, 10]);
    onFilterReset();
  };

  const handleYearRangeChange = (value: number[]) => {
    setYearRange([value[0], value[1]]);
  };

  const handleRatingRangeChange = (value: number[]) => {
    setRatingRange([value[0], value[1]]);
  };

  const getGenreName = (id?: number) => {
    return genres.find(g => g.id === id)?.name;
  };

  const getCountryName = (id?: number) => {
    return countries.find(c => c.id === id)?.name;
  };

  const isDefaultYearRange = () => {
    return (filters.start_year === 1890 || !filters.start_year) && 
           (filters.end_year === currentYear || !filters.end_year);
  };

  const isDefaultRatingRange = () => {
    return (filters.min_rating === 1 || !filters.min_rating) && 
           (filters.max_rating === 10 || !filters.max_rating);
  };

  return (
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
        <Button onClick={handleSearch} disabled={!localSearchQuery.trim() || isLoading}>
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
              <Button onClick={handleFilterApply} disabled={isLoading}>
                Применить фильтры
              </Button>
              <Button variant="outline" onClick={handleFilterReset} disabled={isLoading}>
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
                onClick={() => onFilterRemove('query' as any)}
              >
                ×
              </Button>
            </Badge>
          )}
          
          {filters.genre_id && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Жанр: {getGenreName(filters.genre_id)}
              <Button
                variant="ghost"
                size="sm"
                className="h-auto p-0 ml-1"
                onClick={() => onFilterRemove('genre_id')}
              >
                ×
              </Button>
            </Badge>
          )}

          {filters.country_id && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Страна: {getCountryName(filters.country_id)}
              <Button
                variant="ghost"
                size="sm"
                className="h-auto p-0 ml-1"
                onClick={() => onFilterRemove('country_id')}
              >
                ×
              </Button>
            </Badge>
          )}

          {/* Год выпуска (скрываем если дефолтные значения) */}
          {!isDefaultYearRange() && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Год: {filters.start_year}-{filters.end_year}
              <Button
                variant="ghost"
                size="sm"
                className="h-auto p-0 ml-1"
                onClick={() => onFilterRemove('start_year')}
              >
                ×
              </Button>
            </Badge>
          )}
          
          {/* Рейтинг (скрываем если дефолтные значения) */}
          {!isDefaultRatingRange() && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Рейтинг: {filters.min_rating}-{filters.max_rating}
              <Button
                variant="ghost"
                size="sm"
                className="h-auto p-0 ml-1"
                onClick={() => onFilterRemove('min_rating')}
              >
                ×
              </Button>
            </Badge>
          )}

          <Button
            variant="ghost"
            size="sm"
            onClick={handleFilterReset}
            className="text-muted-foreground"
            disabled={isLoading}
          >
            Очистить все
          </Button>
        </div>
      )}
    </div>
  );
}